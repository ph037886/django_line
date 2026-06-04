from django.db import models

# Create your models here.

class UserInfo(models.Model): #盤點者資訊
    user_id=models.CharField(max_length=20, primary_key=True, help_text='盤點者帳號，用於登陸用')
    user_id2 = models.CharField(max_length=20, null=True, blank=True, help_text='第二帳號，當環境可能同時擁有多個帳號的時候')
    user_name= models.CharField(max_length=20, null=False, blank=True, help_text='姓名')
    
    def __str__(self):
        return self.user_name
    
class ItemInfo(models.Model): #從基本檔匯入資料
    item_diacode = models.CharField(max_length=10, null=False, blank=False, primary_key=True, help_text='品項代碼，主鍵')
    item_english_name = models.CharField(max_length=50, null=False, blank=False, help_text='英文商品名')
    item_chinese_name = models.CharField(max_length=50, null=False, blank=False, help_text='中文商品名')
    item_chemical_name = models.CharField(max_length=50, null=False, blank=False, help_text='學名')
    
    def __str__(self):
        return self.item_english_name
    
class ItemSite(models.Model): #櫃位，is_
    is_id=models.AutoField(primary_key=True, help_text='序號，自動ID')
    is_diacode = models.ForeignKey(ItemInfo, on_delete=models.PROTECT, related_name='diacode_site', help_text='品項代碼')
    is_site= models.CharField(max_length=10, null=False, blank=False, help_text='櫃位')
    
class ItemPackage(models.Model): #單位包裝藥品含量，讓前台可以計算，ip_
    ip_id=models.AutoField(primary_key=True, help_text='序號，自動ID')
    ip_diacode = models.ForeignKey(ItemInfo, on_delete=models.PROTECT, related_name='diacode_package', help_text='品項代碼')
    ip_package_name = models.IntegerField(choices=[(1,'排'), (2, '盒'), (3, '箱')], null=False, blank=False, help_text='包裝名稱，如：排、盒、箱')
    ip_package_count = models.IntegerField(null=False, blank=False, help_text='單位數量，如：一排14顆，輸入14')
    
    
class InventorySession(models.Model): #盤點批次，session_
    session_id = models.AutoField(primary_key=True, help_text='序號，自動ID')
    session_name = models.CharField(max_length=50, help_text='盤點活動名稱，建議輸入民國年月，方便辨識，如：115年6月')
    session_yearmonth = models.IntegerField(help_text='盤點年月，民國年，EX：11501')
    session_is_active = models.BooleanField(default=True, help_text='活動是否啟用')
    session_created_at = models.DateTimeField(auto_now_add=True, help_text='盤點活動創造日期')
    
    def __str__(self):
        return self.session_name

class NeedInventoryMonth(models.Model): #每月需盤點品項，每月匯入，nim_
    nim_id=models.AutoField(primary_key=True, help_text='序號，自動ID')
    nim_yearmonth = models.ForeignKey(InventorySession, on_delete=models.PROTECT, related_name='session_month', help_text='盤點活動')
    nim_diacode = models.ForeignKey(ItemInfo, on_delete=models.PROTECT, related_name='diacode_month', help_text='品項代碼')
    
    constraints = [
        models.UniqueConstraint(
            fields=['nim_yearmonth', 'nim_diacode'],
            name='unique_inventory_month_item'
        )
    ]
    
class InventoryRocord(models.Model): #盤點紀錄，ir_
    ir_id=models.AutoField(primary_key=True, help_text='序號，自動ID')
    ir_diacode=models.ForeignKey(ItemInfo, on_delete=models.PROTECT, related_name='diacode_record', help_text='品項代碼')
    ir_site = models.CharField(max_length=10, blank=True, help_text='櫃位，由哪個櫃位盤點到，也可能是空白')
    ir_count = models.DecimalField(max_digits=8, decimal_places=2, help_text='盤點量，接受半顆或1/4顆')
    ir_user = models.ForeignKey(UserInfo, on_delete=models.PROTECT, related_name='record_user', help_text='盤點者')
    ir_datetime = models.DateTimeField(null=False, blank=False, auto_now_add=True, help_text='盤點資料輸入時間，前台送出時間')
    ir_session = models.ForeignKey(InventorySession, on_delete=models.PROTECT, related_name='record_session')
    
    
