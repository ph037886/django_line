from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import RecruitmentPost, job_bank_link
# Register your models here.


@admin.register(RecruitmentPost)
class RecruitmentPostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)

    list_display = ("title", "short_id", "is_published", "published_at", "updated_at")
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "content")

@admin.register(job_bank_link)
class job_bank_link_admin(admin.ModelAdmin):
    list_display = ("job_name", "job_link", "job_show")
    search_fields = ("job_name",)
    list_filter = ('job_show',)