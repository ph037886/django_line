from django.contrib import admin
from .models import MemberInfo

# Register your models here.

@admin.register(MemberInfo)
class MemberInfoAdmin(admin.ModelAdmin):
    list_display = ("line_id",)