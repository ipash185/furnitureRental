from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    brand = models.CharField(max_length=200, null=False, blank=False, default="No Brand")
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    image = models.ImageField(upload_to='product_image/%y/%m/%d', null=False, blank=False)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
