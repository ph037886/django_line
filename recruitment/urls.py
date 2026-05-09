from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="recruitment_post_list"),
]