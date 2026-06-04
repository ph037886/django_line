from django.contrib import admin
from .models import UserInfo, ItemInfo, ItemSite, ItemPackage, InventorySession, NeedInventoryMonth, InventoryRocord

# Register your models here.
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display=('user_id', 'user_id2', 'user_name',)
    search_fields=('user_name',)
    ordering=('user_id',)
    
@admin.register(ItemInfo)
class ItemInfoAdmin(admin.ModelAdmin):
    list_display=('item_diacode', 'item_english_name', 'item_chinese_name', 'item_chemical_name', )
    search_fields=('item_diacode', 'item_english_name', 'item_chinese_name', 'item_chemical_name', )
    ordering=('item_diacode', )    
    
@admin.register(ItemSite)
class ItemSiteAdmin(admin.ModelAdmin):
    list_display=('is_diacode', 'is_site',)
    search_fields=('is_diacode', 'is_site',)
    list_filter=('is_site',)
    ordering=('is_site',)

@admin.register(ItemPackage)
class ItemPackageAdmin(admin.ModelAdmin):
    list_display=('ip_diacode', 'ip_package_name', 'ip_package_count')
    search_fields=('ip_diacode', )
    list_filter=('ip_package_name', 'ip_package_count',)
    ordering=('ip_diacode', )

@admin.register(InventorySession)
class InventorySessionAdmin(admin.ModelAdmin):
    list_display=('session_name', 'session_yearmonth', 'session_is_active', 'session_created_at', )
    search_fields=('session_name', )
    list_filter=('session_is_active',)
    ordering=('session_yearmonth', 'session_created_at',)
    
@admin.register(NeedInventoryMonth)
class NeedInventoryMonthAdmin(admin.ModelAdmin):
    list_display=('nim_yearmonth', 'nim_diacode', )
    search_fields=('nim_yearmonth', 'nim_diacode', )
    list_filter=('nim_yearmonth', 'nim_diacode', )
    ordering=('nim_yearmonth', )
    
@admin.register(InventoryRocord)
class InventoryRocordAdmin(admin.ModelAdmin):
    list_display=('ir_diacode', 'ir_site', 'ir_count', 'ir_user', 'ir_datetime', 'ir_session', )
    search_fields=('ir_diacode', 'ir_site', )
    list_filter=('ir_diacode', 'ir_site', 'ir_user', 'ir_session')
    ordering=('ir_datetime', )
    