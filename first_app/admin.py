from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Car)
# admin.site.register(models.Brand)

class brandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name', 'slug']

admin.site.register(models.Brand, brandAdmin)
# admin.site.register(models.Comment)
