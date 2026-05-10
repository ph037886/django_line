from django.urls import path
from . import views

app_name = "recruitment"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    

    path(
        "<uuid:post_uuid>/",
        views.post_detail,
        name="post_detail"
    ),
    
    path("<str:short_id>/", views.post_detail, name="post_detail"),
]