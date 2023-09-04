import openai
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from .forms import AppSettingsForm
from .models import ExceptionLog, AppSettings
from datetime import datetime


def superuser_check(user):
    return user.is_superuser


@user_passes_test(superuser_check)
def exception_list(request):
    if not AppSettings.objects.exists():
        return redirect('exceptbot-settings')
    settings = AppSettings.objects.all().first()
    logs = ExceptionLog.objects.filter(is_resolved=False).order_by('-timestamp')
    return render(request, 'exceptbot/list.html', {'logs': logs, 'settings': settings})


@user_passes_test(superuser_check)
def exception_resolved(request):
    logs = ExceptionLog.objects.filter(is_resolved=True).order_by('-timestamp')
    return render(request, 'exceptbot/list.html', {'logs': logs})


@user_passes_test(superuser_check)
def mark_resolved(request, log_id):
    log = ExceptionLog.objects.get(id=log_id)
    log.is_resolved = True
    log.resolved_by = request.user
    log.resolved_at = datetime.now()
    log.save()
    return redirect('exceptbot-list')


@user_passes_test(superuser_check)
def exception_detail(request, log_id):
    log = get_object_or_404(ExceptionLog, id=log_id)
    settings = AppSettings.objects.all().first()
    return render(request, 'exceptbot/detail.html', {'log': log, 'settings': settings})


@user_passes_test(superuser_check)
def exception_error_message(request, log_id):
    log = get_object_or_404(ExceptionLog, id=log_id)
    return render(request, 'exceptbot/error_message.html', {'log': log})


@user_passes_test(superuser_check)
def exception_file_content(request, log_id):
    log = get_object_or_404(ExceptionLog, id=log_id)
    return render(request, 'exceptbot/file_content.html', {'log': log})


@user_passes_test(superuser_check)
def ai_recommendation(request, log_id):
    log = get_object_or_404(ExceptionLog, id=log_id)
    settings = AppSettings.objects.all().first()
    openai.api_key = settings.openai_api_key

    if not log.ai_suggestion:

        exeption_information = f"""
        My Django application has thrown an exception.
        An exception happened in line {log.line_number} of file {log.file_name}.
        The exception type is: {log.exception_type}
        The content of the exception message is:
        ```
        {log.full_error_message}
        ```
        The content of the file that produced the exception is:
        ```
        {log.file_content}
        ```
        The specific line from the above that threw the error is:
        ```
        {log.error_line_content}
        ```
        Please provide a suggestion for how to address the issue.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model='gpt-4',
            messages=[
                {"role": "system",
                 "content": """You are ExceptBot. Users send you information about exceptions in their Django applications
                 and you respond with useful instructions and code on how to fix the issue. Please answer efficiently
                 and use an economy of words."""
                 },
                {"role": "user",
                 "content": exeption_information
                 }
            ],
        )

        log.ai_suggestion = response['choices'][0]['message']['content']
        log.save()

    return render(request, 'exceptbot/ai_suggestion.html', {'log': log})


@user_passes_test(superuser_check)
def app_settings_view(request):
    settings, created = AppSettings.objects.get_or_create()

    if request.method == "POST":
        form = AppSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('exceptbot-list')
    else:
        form = AppSettingsForm(instance=settings)

    return render(request, 'exceptbot/settings.html', {'form': form})

