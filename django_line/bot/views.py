from django.shortcuts import render

# Create your views here.
import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import MemberInfo

@csrf_exempt
def line_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    body = request.body

    try:
        payload = json.loads(body.decode("utf-8"))
    except:
        return HttpResponseBadRequest("Invalid JSON")

    events = payload.get("events", [])

    for event in events:
        event_type = event.get("type")

        # ✅ 重點：follow event
        if event_type == "follow":
            user_id = event["source"]["userId"]

            print("New follow:", user_id)

            MemberInfo.objects.update_or_create(
                line_id=user_id,
                defaults={
                    "is_blocked": False
                }
            )

        # 🔁 block / unfollow
        if event_type == "unfollow":
            user_id = event["source"]["userId"]

            MemberInfo.objects.filter(line_id=user_id).update(
                is_blocked=True
            )

    return JsonResponse({"status": "ok"})