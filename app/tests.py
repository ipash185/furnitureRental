from django.test import TestCase
from django.urls import reverse, resolve
from . import views

# Create your tests here.

class TestUrls(TestCase):

    def test_home_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.home)

    def test_product_detail_url_resolves(self):
        url = reverse('product_detail', args=[1])  # Assuming product_id is 1
        self.assertEqual(resolve(url).func, views.products_detail)

    def test_rent_url_resolves(self):
        url = reverse('rent', args=[1])  # Assuming product_id is 1
        self.assertEqual(resolve(url).func, views.rent)

    def test_my_rent_products_url_resolves(self):
        url = reverse('my_rent_products')
        self.assertEqual(resolve(url).func, views.my_rent_products)

    def test_cancel_rent_url_resolves(self):
        url = reverse('cancel_rent', args=[1])  # Assuming rent_id is 1
        self.assertEqual(resolve(url).func, views.cancel_rent)

    def test_product_damaged_url_resolves(self):
        url = reverse('product_damaged', args=[1])  # Assuming rent_id is 1
        self.assertEqual(resolve(url).func, views.product_damaged)

    # Add tests for other URLs following the same pattern

    # Add more tests for static and media URLs if needed
