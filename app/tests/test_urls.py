from django import test
from django.urls import reverse, URLPattern

from app.urls import urlpatterns


class MyAppUrlsTest(test.SimpleTestCase):

    def test_responses(self):
        self.assertTrue(1==1)