from django.db import models


class RedirectCode(models.Model):
    url = models.URLField(max_length=500, null=False, blank=False)
    code = models.CharField(max_length=20, null=False, db_index=True, unique=True)

    def __str__(self):
        url_snippet = self.url[:20]
        if len(self.url) > 20:
            url_snippet += '...'
        return '{}: {}'.format(
            self.code,
            url_snippet
        )

    class Meta:
        db_table = 'redirect_code'
