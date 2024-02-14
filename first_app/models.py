from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Car(models.Model):
    brand = models.ForeignKey(Brand,on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.ImageField()
    
    def __str__(self):
        return self.name