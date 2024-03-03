from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Catagory = models.ForeignKey(Catagory,on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    Book =  models.ForeignKey(Book, on_delete = models.CASCADE, related_name='comment')
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"Commented by {self.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)