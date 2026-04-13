from django.urls import path
from .views import liff_register_page, member_register_api

urlpatterns = [
    path("liff/register/", liff_register_page, name="liff_register_page"),
    path("api/member/register/", member_register_api, name="member_register_api"),
]