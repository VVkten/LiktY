from django.contrib import admin
from .models import Author, Category, Product, Cart, Order, OrderItem, Seller
from django.contrib.auth.models import User
admin.site.register(Seller)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)

