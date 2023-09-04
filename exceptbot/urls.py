"""
URL configuration for ExceptBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import exception_list, mark_resolved, exception_detail, exception_error_message, exception_file_content, \
    exception_resolved, ai_recommendation, app_settings_view

urlpatterns = [
    path('exceptbot/', exception_list, name='exceptbot-list'),
    path('exceptbot/resolved', exception_resolved, name='exceptbot-resolved'),
    path('exceptbot/<int:log_id>/resolve/', mark_resolved, name='exceptbot-mark-resolved'),
    path('exceptbot/<int:log_id>/ai/', ai_recommendation, name='exceptbot-ai-recommendation'),
    path('exceptbot/<int:log_id>/', exception_detail, name='exceptbot-exception-detail'),
    path('exceptbot/<int:log_id>/error/', exception_error_message, name='exceptbot-error-message'),
    path('exceptbot/<int:log_id>/file/', exception_file_content, name='exceptbot-file-content'),
    path('exceptbot/settings/', app_settings_view, name='exceptbot-settings'),  # new line here
]
