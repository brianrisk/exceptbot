from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.core.exceptions import PermissionDenied
from .models import ExceptionLog
from .views import exception_list, exception_detail, mark_resolved
from .middleware import ExceptBotMiddleware


class ExceptBotTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_exception_list_view_renders(self):
        request = self.factory.get('/exceptbot/')
        response = exception_list(request)
        self.assertEqual(response.status_code, 200)

    def test_exception_detail_view_renders(self):
        # You might need to create an ExceptionLog instance first.
        # Create a test user (this assumes you have a user model,
        # typically from 'django.contrib.auth.models' in standard Django setups)
        test_user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        log = ExceptionLog.objects.create(
            exception_type='TestException',
            message='This is a test',
            traceback='Traceback (most recent call last): ...',  # Placeholder traceback
            url_path='/some/test/url/',
            file_name='test_file.py',
            file_content='def fake_function():\n    raise TestException("This is a test")',
            user=test_user
        )
        request = self.factory.get(f'/exceptbot/{log.id}/')
        response = exception_detail(request, log_id=log.id)
        self.assertEqual(response.status_code, 200)

    def test_exception_is_logged_by_middleware(self):
        middleware = ExceptBotMiddleware(lambda r: PermissionDenied())  # Mock view that raises an exception.
        request = self.factory.get('/some_url/')

        # Trigger the middleware.
        with self.assertRaises(PermissionDenied):
            middleware(request)

        # Check if exception was logged.
        self.assertEqual(ExceptionLog.objects.count(), 1)

