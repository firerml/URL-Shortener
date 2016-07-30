import base64
import hashlib
from time import time

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
