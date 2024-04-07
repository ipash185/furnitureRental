from django import test
from django.urls import reverse, URLPattern

from app.urls import urlpatterns


class MyAppUrlsTest(test.SimpleTestCase):

    def test_responses(self):
        for url in urlpatterns:
            # For now, perform only GET requests and ignore URLs that need arguments.
            if not isinstance(url, URLPattern) or url.pattern.regex.groups or not url.name:
                continue
            urlpath = reverse(url.name)
            response = self.client.get(urlpath, follow=True)
            self.assertEqual(response.status_code, 200)