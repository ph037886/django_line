#python manage.py makemigrations
#python manage.py migrate
from django.db import models

# Create your models here.

class MemberInfo(models.Model):
    line_id = models.CharField(max_length=100, unique=True, db_index=True) #line ID
    name = models.CharField(max_length=200, unique=False) #姓名
    phone = models.CharField(max_length=30, blank=True) #電話
    email = models.EmailField(blank=True) #E-mail
    graduate_year = models.IntegerField(null=True, blank=True, db_index=True) #畢業年
    is_blocked = models.BooleanField(default=False) #是否封鎖，封鎖就不傳送，預設否
    created_at = models.DateTimeField(auto_now_add=True) #資料建立時間
    line_display_name = models.CharField(max_length=100, blank=True) #line顯示名稱
    consent_recruitment = models.BooleanField(default=False) #是否願意接受徵才訊息

    def __str__(self):
        return self.line_id

    class Meta:
        db_table = "member_info"