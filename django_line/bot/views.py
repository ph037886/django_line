from django.shortcuts import render

# Create your views here.
import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import MemberInfo


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
    phone = payload.get("phone", "").strip()
    email = payload.get("email", "").strip()
    graduate_year = payload.get("graduate_year")

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
            "phone": phone,
            "email": email,
            "graduate_year": graduate_year_value,
            "is_blocked": False,
        }
    )

    return JsonResponse({
        "status": "ok",
        "message": "資料已儲存"
    })