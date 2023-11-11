from django.contrib.auth import get_user_model, login
from django.conf import settings


class AutoSuperuserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only run if in DEBUG mode to avoid creating superusers in production
        if settings.DEBUG:
            User = get_user_model()
            # Check if there are no superusers and create one if necessary
            if not User.objects.filter(is_superuser=True).exists():
                superuser = User.objects.create_superuser(
                    'admin', 'admin@example.com', 'adminpassword'
                )
                login(request, superuser, backend='django.contrib.auth.backends.ModelBackend')
            else:
                # If a superuser exists, log in the first one found
                superuser = User.objects.filter(is_superuser=True).first()
                login(request, superuser, backend='django.contrib.auth.backends.ModelBackend')

        response = self.get_response(request)
        return response
