from django.shortcuts import render

# Create your views here.
import base64
import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def verify_line_signature(body: bytes, signature: str, channel_secret: str) -> bool:
    hash = hmac.new(
        channel_secret.encode("utf-8"),
        body,
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash).decode("utf-8")
    return hmac.compare_digest(expected_signature, signature)


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
        print("LINE EVENT:", json.dumps(event, ensure_ascii=False))

    return JsonResponse({"status": "ok"})