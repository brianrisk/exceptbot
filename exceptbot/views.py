from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import ExceptionLog
from datetime import datetime


def superuser_check(user):
    return user.is_superuser


@user_passes_test(superuser_check)
def exception_list(request):
    logs = ExceptionLog.objects.filter(is_resolved=False).order_by('-timestamp')
    return render(request, 'ExceptBot/list.html', {'logs': logs})


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
    return render(request, 'ExceptBot/detail.html', {'log': log})
