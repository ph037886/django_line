from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import RecruitmentPost
# Register your models here.


@admin.register(RecruitmentPost)
class RecruitmentPostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)

    list_display = ("title", "is_published", "published_at", "updated_at")
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "content")