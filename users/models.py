from django.db import models
from django.contrib.auth.models import User


class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=False, null=False)
    delivery_address = models.CharField(
        max_length=100, blank=False, null=False)

    def __str__(self):
        return self.user
