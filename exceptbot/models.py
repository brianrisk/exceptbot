import re

from django.contrib.auth.models import User
from django.db import models


class ExceptionLog(models.Model):
    url_path = models.TextField()
    exception_type = models.CharField(max_length=255)
    full_error_message = models.TextField(blank=True)
    file_name = models.CharField(max_length=255)
    file_content = models.TextField()
    line_number = models.PositiveIntegerField(null=True, blank=True)
    error_line_content = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name='caused_exceptions', null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, related_name='resolved_exceptions', null=True, blank=True, on_delete=models.SET_NULL)
    resolved_at = models.DateTimeField(null=True, blank=True)
    ai_suggestion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.exception_type} at {self.url_path}"

    def get_blocks(self):
        # Split the content into blocks
        blocks = re.split(r'(```[a-zA-Z]*\n)', self.ai_suggestion)

        # Iterate over the blocks
        formatted_blocks = []
        in_code_block = False
        language = None
        for block in blocks:
            if block.startswith('```'):  # This block contains the language
                in_code_block = not in_code_block

                # Extract the language from the block and remove the backticks and newline
                language = block[3:].strip()
                if language == '':
                    language = None
            elif in_code_block:  # This is a code block
                formatted_blocks.append({
                    'text': block.strip(),
                    'is_code': True,
                    'language': language,
                })
            else:  # This is not a code block
                formatted_blocks.append({
                    'text': block,
                    'is_code': False,
                    'language': None,
                })

        return formatted_blocks


class AppSettings(models.Model):
    openai_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="Required for AI recommendations.  Get an OpenAI account; google 'openai api key'")
    base_url = models.CharField(max_length=255, blank=True, null=True, help_text="ex: https://exceptbot.com")
    project_name = models.CharField(max_length=255, blank=True, null=True, help_text="The directory name of your project. Ex: 'exceptbot'")