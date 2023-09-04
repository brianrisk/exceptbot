from django import forms
from .models import AppSettings


class AppSettingsForm(forms.ModelForm):
    class Meta:
        model = AppSettings
        fields = ['openai_api_key', 'base_url', 'project_name']
