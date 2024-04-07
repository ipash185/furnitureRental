from django.test import TestCase
from django.urls import reverse
from .models import Product, Rent

class URLTests(TestCase):
    def setUp(self):
        # Set up any necessary test data
        self.product = Product.objects.create(name='Test Product', price=100)

    def test_home_url(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.client.get(reverse('product_detail', args=(self.product.id,)))
        self.assertEqual(response.status_code, 200)

    # Add more test cases for other URLs...

    def test_static_media_url(self):
        response = self.client.get(settings.MEDIA_URL + 'test_image.jpg')
        self.assertEqual(response.status_code, 200)

    def test_static_url(self):
        response = self.client.get(settings.STATIC_URL + 'test.css')
        self.assertEqual(response.status_code, 200)