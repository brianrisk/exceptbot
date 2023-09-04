import sys
import traceback
from .models import ExceptionLog


class ExceptBotMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Get the current stack trace
        current_traceback = traceback.extract_stack()

        # Loop through the stack trace in reverse to find the last occurrence
        # of a file that is part of your Django project
        for stack in reversed(current_traceback):
            if 'dat' in stack.filename:
                # If you find a file from your project, log the relevant information
                file_name = stack.filename
                line_number = stack.lineno
                error_line_content = stack.line
                break
        else:
            # If no project file found in the stack trace, log the last entry
            stack = current_traceback[-1]
            file_name = stack.filename
            line_number = stack.lineno
            error_line_content = stack.line

        exc_type, exc_value, exc_traceback = sys.exc_info()
        full_error_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        url_path = request.path
        exception_type = str(type(exception).__name__)
        # tb = traceback.extract_tb(exception.__traceback__)[-1]

        with open(file_name, 'r') as file:
            file_content = file.read()
        user = request.user if request.user.is_authenticated else None

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
