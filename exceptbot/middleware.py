import traceback
from .models import ExceptionLog


class ExceptBotMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        url_path = request.path
        exception_type = str(type(exception).__name__)
        file_name = traceback.extract_tb(exception.__traceback__)[-1].filename
        with open(file_name, 'r') as file:
            file_content = file.read()
        user = request.user if request.user.is_authenticated else None

        ExceptionLog.objects.create(
            url_path=url_path,
            exception_type=exception_type,
            file_name=file_name,
            file_content=file_content,
            user=user
        )
