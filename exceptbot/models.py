from django.contrib.auth.models import User
from django.db import models


class ExceptionLog(models.Model):
    url_path = models.TextField()
    exception_type = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_content = models.TextField()
    user = models.ForeignKey(User, related_name='caused_exceptions', null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, related_name='resolved_exceptions', null=True, blank=True, on_delete=models.SET_NULL)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.exception_type} at {self.url_path}"


class AppSettings():
    openai_api_key = models.CharField(max_length=255, blank=True, null=True)
    base_url = models.CharField(max_length=255, blank=True, null=True)