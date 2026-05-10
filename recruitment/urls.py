from django.urls import path
from . import views

app_name = "recruitment"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    
    path("<str:post_short_id>/", views.post_detail, name="post_detail"),
]