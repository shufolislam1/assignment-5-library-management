from django.contrib import admin
from .models import  BorrowingHistory, Comment,  UserAccountModel

# Register your models here.
# admin.site.register(Transaction)
admin.site.register(BorrowingHistory)
admin.site.register(Comment)
admin.site.register(UserAccountModel)

