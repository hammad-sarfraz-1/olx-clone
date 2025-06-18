# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductFieldViewSet,
    ProductViewSet,
    SubcategoryViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"subcategories", SubcategoryViewSet)
router.register(r"products", ProductViewSet, basename="product")
router.register(r"product-fields", ProductFieldViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
