from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    OrderViewSet,
    ProductFieldViewSet,
    ProductViewSet,
    SubcategoryViewSet,
    UserProfileViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"subcategories", SubcategoryViewSet, basename="subcategory")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"product-fields", ProductFieldViewSet, basename="productfield")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"profiles", UserProfileViewSet, basename="userprofile")

urlpatterns = [
    path("", include(router.urls)),
]
