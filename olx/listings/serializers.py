# serializers.py
from rest_framework import serializers

from .models import (
    Category,
    Order,
    OrderItem,
    Product,
    ProductField,
    Subcategory,
    UserProfile,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class ProductFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductField
        fields = ["key", "value"]


class ProductSerializer(serializers.ModelSerializer):
    fields = ProductFieldSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "subcategory",
            "title",
            "description",
            "price",
            "created_at",
            "fields",
        ]
        read_only_fields = ["id", "created_at", "user"]

    def create(self, validated_data):
        fields_data = validated_data.pop("fields")
        product = Product.objects.create(**validated_data)
        for field in fields_data:
            ProductField.objects.create(product=product, **field)
        return product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "price"]
        read_only_fields = ["id", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "items"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        buyer = self.context["request"].user

        if not items_data:
            raise serializers.ValidationError("Order must contain at least one item.")

        order = Order.objects.create(buyer=buyer)

        for item in items_data:
            product = item.get("product")

            if isinstance(product, Product):
                product_obj = product
            else:
                try:
                    product_obj = Product.objects.get(id=product)
                except Product.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Product ID {product} not found."
                    )

            if product_obj.is_sold:
                raise serializers.ValidationError(
                    f"{product_obj.title} is already sold."
                )

            OrderItem.objects.create(
                order=order, buyer=buyer, product=product_obj, price=product_obj.price
            )

            product_obj.is_sold = True
            product_obj.save()

        return order


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone", "address"]
