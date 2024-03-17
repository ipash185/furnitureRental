from django.conf.urls import include
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html',
                                              success_url='change-password-done'), name='change-password'
    ),
    path(
        'change-password-done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/success_password_change.html'),
        name='change-password-done'
    ),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('billing-address', views.billingAddress, name='billing-address'),
    path('edit-billing-address', views.edit_billing_address, name='edit-billing-address'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
]
