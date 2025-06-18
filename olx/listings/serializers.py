# serializers.py
from rest_framework import serializers

from .models import Category, Product, ProductField, Subcategory


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
