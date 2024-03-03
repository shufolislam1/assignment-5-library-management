from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Book)
# admin.site.register(models.Catagory)

class CatagoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name', 'slug']

admin.site.register(models.Catagory, CatagoryAdmin)
# admin.site.register(models.Comment)
