from django.contrib import admin
from .models import MemberInfo, RecruitmentEvent

# Register your models here.

@admin.register(MemberInfo)
class MemberInfoAdmin(admin.ModelAdmin):
    list_display = ("line_id", "name", "phone", "email", "graduate_year", "is_blocked", "created_at", "live_site")
    search_fields = ("line_id", "name", "phone", "email")
    list_filter = ("graduate_year", "is_blocked", "created_at", "live_site")
    
@admin.register(RecruitmentEvent)
class RecruitmentEventAdmin(admin.ModelAdmin):
    list_display=("event_date", "event_name")
    search_fields=("event_date", "event_name")
    list_filter=("event_date", "event_name")