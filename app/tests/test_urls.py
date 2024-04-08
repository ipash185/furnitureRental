from django.test import TestCase
from django.urls import reverse, resolve
from .. import views

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

    def test_return_request_url_resolves(self):
        url = reverse('return_request', args=[1])  # Assuming rent_id is 1
        self.assertEqual(resolve(url).func, views.return_request)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, views.search)

    def test_delete_comment_url_resolves(self):
        url = reverse('delete_comment', args=[1])  # Assuming comment_id is 1
        self.assertEqual(resolve(url).func, views.delete_comment)

    def test_billing_url_resolves(self):
        url = reverse('billing', args=[1])  # Assuming product_id is 1
        self.assertEqual(resolve(url).func, views.billing)

    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, views.dashboard)

    def test_view_notifications_url_resolves(self):
        url = reverse('view_notifications')
        self.assertEqual(resolve(url).func, views.view_notifications)

    def test_delete_notification_url_resolves(self):
        url = reverse('delete_notification', args=[1])  # Assuming notification_id is 1
        self.assertEqual(resolve(url).func, views.delete_notification)

    def test_add_product_url_resolves(self):
        url = reverse('add_product')
        self.assertEqual(resolve(url).func, views.add_product)

    def test_delete_product_url_resolves(self):
        url = reverse('delete_product', args=[1])  # Assuming product_id is 1
        self.assertEqual(resolve(url).func, views.delete_product)

    def test_edit_product_url_resolves(self):
        url = reverse('edit_product', args=[1])  # Assuming product_id is 1
        self.assertEqual(resolve(url).func, views.edit_product)

    def test_pending_rent_request_url_resolves(self):
        url = reverse('pending_rent_requests')
        self.assertEqual(resolve(url).func, views.pending_rent_requests)

    def test_accepted_rent_request_url_resolves(self):
        url = reverse('accepted_rent_requests', args=[1])   # Assuming rent_id is 1
        self.assertEqual(resolve(url).func, views.accept_rent_request)

    def test_rejected_rent_request_url_resolves(self):
        url = reverse('rejected_rent_requests', args=[1])   # Assuming rent_id is 1
        self.assertEqual(resolve(url).func, views.reject_rent_request)

    def test_delivery_rented_products_url_resolves(self):
        url = reverse('delivery_rented_products')
        self.assertEqual(resolve(url).func, views.delivery_rented_products)

    def test_delivered_rented_products_url_resolves(self):
        url = reverse('delivered_rented_products', args=[1])    # Assuming rent_id is 1
        self.assertEqual(resolve(url).func, views.delivered_rented_products)

    def test_rented_products_url_resolves(self):
        url = reverse('rented_products')
        self.assertEqual(resolve(url).func, views.rented_products)

    def test_accept_return_request_url_resolves(self):
        url = reverse('accept_return_request', args=[1])    # Assuming rent_id is 1
        self.assertEqual(resolve(url).func, views.accept_return_request)

    def test_all_rent_return_request_url_resolves(self):
        url = reverse('all_rent_return_requests')
        self.assertEqual(resolve(url).func, views.all_rent_request)

    def test_return_product_url_resolves(self):
        url = reverse('return_product')
        self.assertEqual(resolve(url).func, views.return_product)

    def test_all_rent_url_resolves(self):
        url = reverse('all_rent')
        self.assertEqual(resolve(url).func, views.activity)

    def test_virtual_url_resolves(self):
        url = reverse('virtual')
        self.assertEqual(resolve(url).func, views.virtual)

    # Add more tests for static and media URLs if needed
