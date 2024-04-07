from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from .. import views

class TestUrls(TestCase):

    def test_change_password_url_resolves(self):
        url = reverse('change-password')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordChangeView)
        
    def test_change_password_done_url_resolves(self):
        url = reverse('change-password-done')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordChangeDoneView)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, views.profile)

    def test_billing_address_url_resolves(self):
        url = reverse('billing-address')
        self.assertEqual(resolve(url).func, views.billingAddress)

    def test_edit_billing_address_url_resolves(self):
        url = reverse('edit-billing-address')
        self.assertEqual(resolve(url).func, views.edit_billing_address)

    def test_edit_profile_url_resolves(self):
        url = reverse('edit-profile')
        self.assertEqual(resolve(url).func, views.edit_profile)
