from django.contrib.auth.models import User
from django.db import models
from app.models import Product


class Rent(models.Model):

    class Status(models.TextChoices):
        pending = 'pending', 'Pending'
        rented = 'rented', 'Rented'
        rejected = 'rejected', 'Rejected'
        returned = 'returned', 'Returned'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    rental_day = models.IntegerField(default=0)
    is_rented = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.pending)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.product}'
