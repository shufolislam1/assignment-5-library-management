from django.contrib import admin
from .models import Transaction, BorrowingHistory, Comment

# Register your models here.
admin.site.register(Transaction)
admin.site.register(BorrowingHistory)
admin.site.register(Comment)
