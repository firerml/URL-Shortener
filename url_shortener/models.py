import base64
import hashlib
import logging
from time import time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class RedirectCode(models.Model):
    url = models.URLField(max_length=500, db_index=True)
    code = models.CharField(max_length=20, db_index=True, unique=True)

    def __str__(self):
        url_snippet = self.url[:20]
        if len(self.url) > 20:
            url_snippet += '...'
        return '{}: {}'.format(
            self.code,
            url_snippet
        )

    def get_short_url(self):
        return '{}/{}'.format(settings.DOMAIN, self.code)

    @staticmethod
    def generate_code():
        """
        Generates a hashed, url-safe base64 code. The code is truncated to 8 characters,
        which still allows for trillions of results, but just to be safe it ensures the code is unique,
        regenerating it if it's a dupe.
        """
        # Since we'll be truncating the
        while True:
            # Hash the current time (seconds since the epoch).
            current_time = str(time()).encode()
            sha1_hash = hashlib.sha1(current_time).digest()
            # Convert the hash to a user and url friendly string code.
            code = base64.urlsafe_b64encode(sha1_hash).decode()[:8]
            if not RedirectCode.objects.filter(code=code).exists():
                break
        return code

    class Meta:
        db_table = 'redirect_code'


    @staticmethod
    def get_or_create_from_url(url):
        """
        With a url, create (or get if dupe url) a RedirectCode object.
        :return: dict of info, containing RedirectCode object (or None if errors), error message (or empty string),
        and created.
        """
        return_info = {
            'error': '',
            'redirect_code_object': None,
            'created': False
        }
        # Create a RedirectCode object and populate the context to display a success (or error) message.
        if not url:
            return_info['error'] = 'URL cannot be blank!'
            return return_info

        # See if this URL has been used before.
        redirect_code_obj = RedirectCode.objects.filter(url=url).first()
        # If not, create a new RedirectCode object and validate it, preparing error messages if there are any.
        if not redirect_code_obj:
            return_info['created'] = True
            redirect_code_obj = RedirectCode(url=url, code=RedirectCode.generate_code())
            try:
                # Validate that the user-provided URL is in valid format.
                redirect_code_obj.full_clean()
                redirect_code_obj.save()
                return_info['redirect_code_object'] = redirect_code_obj
            except ValidationError as e:
                url_errors = e.message_dict.get('url')
                if url_errors:
                    return_info['error'] = url_errors[0] + ' (Did you forget the http/https?)'
                else:
                    # There should be no other validation errors, so log it and show user a generic error message.
                    logging.info(e.message_dict)
                    return_info['error'] = 'An error has occurred. Contact firerml@gmail.com to report this bug!'
                    return return_info
        else:
            return_info['redirect_code_object'] = redirect_code_obj
        return return_info
