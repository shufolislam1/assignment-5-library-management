from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    Catagory = models.ManyToManyField(Catagory)
    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user