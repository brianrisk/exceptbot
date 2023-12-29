import sys
import traceback
from django.db import transaction
from .models import ExceptionLog, AppSettings


class ExceptBotMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        app_settings = AppSettings.objects.first()
        project_name = app_settings.project_name if app_settings and app_settings.project_name else ''

        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_traceback = traceback.extract_tb(exc_traceback)

        for stack in reversed(formatted_traceback):
            if project_name and project_name in stack.filename:
                file_name = stack.filename
                line_number = stack.lineno
                error_line_content = stack.line
                break
        else:
            stack = formatted_traceback[-1]
            file_name = stack.filename
            line_number = stack.lineno
            error_line_content = stack.line

        full_error_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        url_path = request.path
        exception_type = str(type(exception).__name__)

        with open(file_name, 'r') as file:
            file_content = file.read()
        user = request.user if request.user.is_authenticated else None

        # Check for existing non-resolved exception
        with transaction.atomic():
            existing_exception = ExceptionLog.objects.filter(
                exception_type=exception_type,
                file_name=file_name,
                is_resolved=False
            ).first()

            if existing_exception:
                existing_exception.count += 1
                existing_exception.save()
            else:
                ExceptionLog.objects.create(
                    url_path=url_path,
                    exception_type=exception_type,
                    full_error_message=full_error_message,
                    file_name=file_name,
                    file_content=file_content,
                    line_number=line_number,
                    error_line_content=error_line_content,
                    user=user,
                )
