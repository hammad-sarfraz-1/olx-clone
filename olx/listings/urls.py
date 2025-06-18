# urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, SubcategoryViewSet, ProductViewSet, ProductFieldViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'products', ProductViewSet, basename='product')  
router.register(r'product-fields', ProductFieldViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
