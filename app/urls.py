from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('home/<int:product_id>/', views.products_detail, name='product_detail'),
    path('home/rent/<int:product_id>/', views.rent, name='rent'),
    path('home/rent/my-rent-products/', views.my_rent_products, name='my_rent_products'),
    path('home/rent/my-rent-products/cancel-product/<int:rent_id>/', views.cancel_rent, name='cancel_rent'),
    path('dashboard/rent/all/rented-products/return/request/<int:rent_id>/', views.return_request,
         name='return_request'),
    path('home/search/', views.search, name='search'),
    path('home/products/comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('home/products/billing/<int:product_id>/', views.billing, name='billing'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-product/', views.add_product, name='add_product'),
    path('dashboard/product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('dashboard/product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('dashboard/rent/request/all/status/pending/', views.pending_rent_requests, name='pending_rent_requests'),
    path('dashboard/rent/all/request/approved/<int:rent_id>/', views.accept_rent_request,
         name='accepted_rent_requests'),
    path('dashboard/rent/all/request/rejected/<int:rent_id>/', views.reject_rent_request,
         name='rejected_rent_requests'),
    path('dashboard/rent/all/wait-for-delivey/', views.delivery_rented_products, name='delivery_rented_products'),
    path('dashboard/rent/all/delivered/<int:rent_id>/', views.delivered_rented_products,
         name='delivered_rented_products'),
    path('dashboard/rent/all/rented-products/', views.rented_products, name='rented_products'),
    path('dashboard/rent/all/rented-products/return/request/accept/<int:rent_id>/', views.accept_return_request,
         name='accept_return_request'),
    path('dashboard/rent/all/rented-products/return/request/', views.all_rent_request, name='all_rent_return_requests'),
    path('dashboard/rent/all/rented-products/return/', views.return_product, name='return_product'),
    path('dashboard/rent/all/', views.activity, name='all_rent'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
