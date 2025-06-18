# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Category, Product, ProductField, Subcategory
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    ProductFieldSerializer,
    ProductSerializer,
    SubcategorySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    # print(queryset)
    serializer_class = SubcategorySerializer
    # print(serializer_class)
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if user.is_superuser:
            return Product.objects.all()

        return Product.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductFieldViewSet(viewsets.ModelViewSet):
    queryset = ProductField.objects.all()

    serializer_class = ProductFieldSerializer
    permission_classes = [IsAuthenticated]
