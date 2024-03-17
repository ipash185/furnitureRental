from django.contrib import admin
from .models import UserInformation


class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'delivery_address')


admin.site.register(UserInformation, UserInformationAdmin)
