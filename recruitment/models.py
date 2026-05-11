from django.db import models
import uuid
from django.utils.text import slugify

def generate_short_uuid():
    return uuid.uuid4().hex[:8]

class RecruitmentPost(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    short_id = models.CharField(
        max_length=8,
        unique=True,
        default=generate_short_uuid,
        editable=False,
        db_index=True,
    )

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title
    
class job_bank_link(models.Model):
    recruitment_post = models.ForeignKey(
        RecruitmentPost,
        on_delete=models.CASCADE,
        related_name="job_bank_links"
    )
    id=models.AutoField(primary_key=True)
    job_name=models.TextField(blank=False)
    job_link=models.URLField(blank=False)
    job_show=models.BooleanField(default=False)
    
    class Meta:
        ordering = ["id"]
    
    def __str__(self):
        return self.job_name