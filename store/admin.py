# store/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Category, Product, Order
from .models import Category, Product, Order, Customer
admin.site.register(Customer)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)

# For users, already registered, but customize if needed
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

