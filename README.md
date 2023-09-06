
<img src="https://d.at/static/exceptbot/github-banner.jpg" width="100%">

# ExceptBot: Django Exception Logger with AI Suggestions for Fixing

**Imagine**: An exception is thrown on your site and it is *critical*.  
You need a solution *fast*.  

ExceptBot is a Django middleware application that captures 
and logs exceptions that occur within your Django project. Site admins
can quickly view exceptions, the code where the problem originated, and 
with a button-click feed all that info to ChatGPT to get a possible solution.

## Features
* Automatically logs exceptions, including:
  * The Python Code and line where the exception occurred
  * The full stack trace
  * URL path, Exception type, timestamp, user (if authenticated)
* Gets AI Suggestions
  * Sends all relevant info to ChatGPT API:
    * Stack trace
    * Source code producing the exception
    * line causing the exception
* Superuser-restricted views to:
  * View a list of unresolved exceptions
  * Mark exceptions as resolved
  * View detailed information for each exception
  * Tracks which superuser resolved an exception and when

## Installation
1. Install the ExceptBot library

```bash
pip3 install exceptbot
```

2. Add 'ExceptBot' to INSTALLED_APPS in your project's `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'exceptbot',
    # ...
]
```

3. Include the middleware in the MIDDLEWARE list in your `settings.py`:

```python
MIDDLEWARE = [
    # ...
    'exceptbot.middleware.ExceptBotMiddleware',
    # ...
]
```

4. Include the ExceptBot URLs in your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
  # ...
  path('', include('exceptbot.urls')),
  # ...
]
```

Run migrations to create the necessary database tables and set up static files

```bash
$ python3 manage.py makemigrations exceptbot
$ python3 manage.py migrate exceptbot
$ python3 manage.py collectstatic --no-input
```

## Usage
Once integrated into your Django project:
* setup the Chat GPT connection (When you have an account, your [API key is here](https://platform.openai.com/account/api-keys))
* Any exception that occurs will be automatically logged by the middleware.
* Superusers can navigate to `/exceptbot/` to view a list of unresolved exceptions.
* Click on an exception to view its detailed information.
* Superusers can mark exceptions as resolved, which will also record who resolved it and when.
