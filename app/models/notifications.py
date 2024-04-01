from django.db import models


class Notifications(models.Model):

    notification = models.CharField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification
