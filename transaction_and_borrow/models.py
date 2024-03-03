from  django.db  import models
from first_app.models import Book
from django.contrib.auth.models import User
# Create your models here.

class Transaction(models.Model):
    book = models.ForeignKey(User, related_name = 'transactions', on_delete = models.CASCADE) # ekjon user er multiple transactions hote pare
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp'] 

class BorrowingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
