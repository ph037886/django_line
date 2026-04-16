from django.contrib import admin
from .models import MemberInfo

# Register your models here.

@admin.register(MemberInfo)
class MemberInfoAdmin(admin.ModelAdmin):
    list_display = ("line_id", "name", "phone", "email", "graduate_year", "is_blocked", "created_at")
    search_fields = ("line_id", "name", "phone", "email")
    list_filter = ("graduate_year", "is_blocked", "created_at")