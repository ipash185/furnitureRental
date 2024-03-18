from django.db import models

class Profit(models.Model):
    investment = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False, blank=False)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False, blank=False)
    
    def __str__(self):
        return self.investment