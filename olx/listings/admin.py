from django.contrib import admin

from .models import (
    Category,
    Order,
    OrderItem,
    Product,
    ProductField,
    Subcategory,
    UserProfile,
)

# Register your models here.

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(ProductField)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
