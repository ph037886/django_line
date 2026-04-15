from django.shortcuts import render

# Create your views here.
import json
import base64
import hashlib
import hmac

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.exceptions import InvalidSignatureError

from .models import MemberInfo

configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


def verify_line_signature(body: bytes, signature: str, channel_secret: str) -> bool:
    hash_value = hmac.new(
        channel_secret.encode("utf-8"),
        body,
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash_value).decode("utf-8")
    return hmac.compare_digest(expected_signature, signature)

def liff_register_page(request):
    return render(request, "bot/liff_register.html")

@csrf_exempt
def member_register_api(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    line_id = payload.get("line_id")
    name = payload.get("name")
    phone = payload.get("phone", "").strip()
    email = payload.get("email", "").strip()
    graduate_year = payload.get("graduate_year")
    consent_recruitment = payload.get("consent_recruitment", False)

    if not line_id:
        return HttpResponseBadRequest("Missing line_id")

    graduate_year_value = None
    if graduate_year not in [None, ""]:
        try:
            graduate_year_value = int(graduate_year)
        except ValueError:
            return HttpResponseBadRequest("graduate_year must be integer")

    MemberInfo.objects.update_or_create(
        line_id=line_id,
        defaults={
            "name": name,
            "phone": phone,
            "email": email,
            "graduate_year": graduate_year_value,
            "consent_recruitment": consent_recruitment,
            "is_blocked": False,
        }
    )

    return JsonResponse({
        "status": "ok",
        "message": "資料已儲存"
    })
    
@csrf_exempt
def line_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    signature = request.headers.get("X-Line-Signature")
    if not signature:
        return HttpResponseBadRequest("Missing signature")

    body = request.body

    if not verify_line_signature(body, signature, settings.LINE_CHANNEL_SECRET):
        return HttpResponseBadRequest("Invalid signature")

    try:
        payload = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    events = payload.get("events", [])

    for event in events:
        event_type = event.get("type")

        if event_type == "follow":
            user_id = event["source"]["userId"]
            reply_token = event["replyToken"]

            MemberInfo.objects.update_or_create(
                line_id=user_id,
                defaults={"is_blocked": False}
            )

            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[
                            TextMessage(
                                text=(
                                    "歡迎加入徵才官方帳號。\n"
                                    "請點以下連結填寫基本資料：\n"
                                    f"{settings.LIFF_REGISTER_URL}"
                                )
                            )
                        ],
                    )
                )

        elif event_type == "unfollow":
            user_id = event["source"]["userId"]
            MemberInfo.objects.filter(line_id=user_id).update(is_blocked=True)

    return JsonResponse({"status": "ok"})

def get_target_members(request):
    targets = MemberInfo.objects.filter(
        graduate_year=2026,
        is_blocked=False,
        consent_recruitment=True
    )

    data = list(
        targets.values(
            "line_id",
            "name",
            "graduate_year",
            "email",
            "phone"
        )
    )

    return JsonResponse({
        "count": len(data),
        "results": data
    })