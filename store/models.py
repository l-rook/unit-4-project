from django.db import models
from django.contrib.auth.models import User
import datetime

class Cat(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Prod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Prod, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return f"Order of {self.quantity} {self.product.name}(s)"
