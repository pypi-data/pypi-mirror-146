from django.contrib import admin

from . import models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('organisation_profile', 'phone_number', 'name', 'email',)
