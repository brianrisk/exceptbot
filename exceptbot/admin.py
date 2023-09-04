from django.contrib import admin
from .models import ExceptionLog, AppSettings

admin.site.register(ExceptionLog)
admin.site.register(AppSettings)
