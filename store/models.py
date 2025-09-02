# store/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username if self.user else "Guest Customer"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True)  # For guest
    address = models.CharField(max_length=200, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Out for Delivery', 'Out for Delivery'),
            ('Received', 'Received'),
            ('Complete', 'Complete'),
        ],
        default='Pending'
    )

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        return self.product.price * self.quantity if self.product else 0