from  django.db  import models
from first_app.models import Book
from django.contrib.auth.models import User
# Create your models here.

# class Transaction(models.Model):
#     user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE, default=1)
#     book = models.ForeignKey(Book, related_name = 'transactions', on_delete = models.CASCADE, default=1)
#     balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
#     amount = models.DecimalField(decimal_places=2, max_digits = 12)
#     balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['timestamp'] 
        
class UserAccountModel(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    
    def __str__(self):
        return str(self.account_no)

class BorrowingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    
    
class Comment(models.Model):
    book =  models.ForeignKey(Book, on_delete = models.CASCADE, related_name='comments', default=1)
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    body = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user', default=1)
    created_on = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"Commented by {self.name}"
