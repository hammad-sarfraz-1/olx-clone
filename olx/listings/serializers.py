from rest_framework import serializers
from .models import Category, Subcategory, Product, ProductField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class ProductFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductField
        fields = ['id', 'key', 'value']


class ProductSerializer(serializers.ModelSerializer):
    fields = ProductFieldSerializer(many=True, required=False)
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Product
        fields = ['id', 'user', 'subcategory', 'title', 'description', 'price', 'created_at']
        # , 'fields'

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        product = Product.objects.create(**validated_data)
        for field in fields_data:
            ProductField.objects.create(product=product, **field)
        return product

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if fields_data is not None:
            instance.fields.all().delete()
            for field in fields_data:
                ProductField.objects.create(product=instance, **field)
        return instance
