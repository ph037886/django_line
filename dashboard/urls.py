from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("members/", views.member_dashboard, name="member_dashboard"),
]