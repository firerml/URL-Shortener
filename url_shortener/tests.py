from django.test import Client, TestCase

from url_shortener.models import RedirectCode


class GetIndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_response(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)


class PostIndexTestCase(TestCase):
    def post_with_url(self, url):
        return self.client.post('/', data={'url': url})

    def setUp(self):
        self.client = Client()

    def test_can_create_new_redirect_code_with_valid_url(self):
        url = 'http://1.com'
        res = self.post_with_url(url)
        self.assertEqual(res.status_code, 201)
        # New RedirectCode was created.
        self.assertTrue(RedirectCode.objects.filter(url=url).exists())
        new_redirect_code = RedirectCode.objects.get(url=url)
        # Code was set on new RedirectCode object.
        self.assertTrue(len(new_redirect_code.code) > 0)

    def test_context_for_template_is_populated(self):
        url = 'http://1.com'
        res = self.post_with_url(url)
        self.assertEqual(res.context.get('original_url'), url)
        code = RedirectCode.objects.first().code
        self.assertEqual(res.context.get('new_url'), 'localhost:5000/c/' + code)

    def test_invalid_urls_return_400_and_do_not_create_redirect_codes(self):
        start_count = RedirectCode.objects.count()

        # Empty url.
        url = ''
        res = self.post_with_url(url)
        self.assertEqual(res.status_code, 400)

        # Non-url string.
        url = 'whyhellothere'
        res = self.post_with_url(url)
        self.assertEqual(res.status_code, 400)

        # No new RedirectCode objects were created.
        self.assertEqual(start_count, RedirectCode.objects.count())

    def test_only_unique_urls_create_new_redirect_codes(self):
        self.assertEqual(RedirectCode.objects.count(), 0)
        res = self.post_with_url('http://1.com')
        # New URLs return 201.
        self.assertEqual(res.status_code, 201)
        self.assertEqual(RedirectCode.objects.count(), 1)
        short_url_1 = res.context.get('new_url')

        res = self.post_with_url('http://1.com')
        # Dupe URLs return 200.
        self.assertEqual(res.status_code, 200)
        self.assertEqual(RedirectCode.objects.count(), 1)
        short_url_2 = res.context.get('new_url')
        self.assertEqual(short_url_1, short_url_2)

        res = self.post_with_url('http://2.com')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(RedirectCode.objects.count(), 2)
        short_url_3 = res.context.get('new_url')
        self.assertNotEqual(short_url_2, short_url_3)

    def test_url_length_difference(self):
        url = 'http://www.OhMyThisIsQuiteALongUrlIndeed.com'
        res = self.post_with_url(url)
        url_length_difference = res.context.get('url_length_difference')
        new_url = res.context.get('new_url')
        self.assertEqual(url_length_difference, len(url) - len(new_url))

        # Difference is 0 if original url is shorter than new one.
        url = 'http://short.com'
        res = self.post_with_url(url)
        url_length_difference = res.context.get('url_length_difference')
        self.assertEqual(url_length_difference, 0)


class RedirectFromCodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = 'http://example.com'
        self.redirect_code = RedirectCode.objects.create(url='http://example.com', code='abc')

    def test_valid_redirect_code_redirects(self):
        res = self.client.get('/c/{}/'.format(self.redirect_code.code))
        self.assertEqual(res['location'], self.url)
        self.assertEqual(res.status_code, 302)
