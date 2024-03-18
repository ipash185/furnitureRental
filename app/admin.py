from django.contrib import admin
from app.models import Product, Comment
from app.models.rent import Rent


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'brand', 'available')
    list_filter = ('available', 'brand', 'created_at', 'updated_at')
    search_fields = ['name', 'brand']


class RentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ['product', 'user']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ['product', 'user']


admin.site.register(Product, ProductAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(Comment, CommentAdmin)
