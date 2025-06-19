# views.py
from django.db import transaction
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import (
    Category,
    Order,
    OrderItem,
    Product,
    ProductField,
    Subcategory,
    UserProfile,
)
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    OrderSerializer,
    ProductFieldSerializer,
    ProductSerializer,
    SubcategorySerializer,
    UserProfileSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductFieldViewSet(viewsets.ModelViewSet):
    queryset = ProductField.objects.all()
    serializer_class = ProductFieldSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Order.objects.all() if user.is_staff else Order.objects.filter(buyer=user)
        )

    def perform_create(self, serializer):
        items_data = self.request.data.get("items")

        if not items_data:
            raise ValidationError("Order must include at least one product.")

        errors = []
        validated_items = []

        with transaction.atomic():
            for item in items_data:
                product_id = item.get("product")

                if not isinstance(product_id, int):
                    errors.append(f"Invalid product ID: {product_id}")
                    continue

                try:
                    product = Product.objects.select_for_update().get(id=product_id)
                except Product.DoesNotExist:
                    errors.append(f"Product with ID {product_id} not found.")
                    continue

                if product.is_sold:
                    errors.append(f"Product '{product.title}' is already sold.")
                    continue

                validated_items.append(product)

            if errors:
                raise ValidationError({"errors": errors})

            order = serializer.save(buyer=self.request.user)

            for product in validated_items:
                OrderItem.objects.create(
                    order=order,
                    buyer=self.request.user,
                    product=product,
                    price=product.price,
                )
                product.is_sold = True
                product.save()


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
