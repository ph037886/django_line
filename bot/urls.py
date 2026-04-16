from django.urls import path
from .views import line_webhook, liff_register_page, member_register_api, get_target_members

urlpatterns = [
    path("webhook/", line_webhook, name="line_webhook"),
    path("liff/register/", liff_register_page, name="liff_register_page"),
    path("api/member/register/", member_register_api, name="member_register_api"),
    path("api/member/targets/", get_target_members, name="get_target_members"),
]