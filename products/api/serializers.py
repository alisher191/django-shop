from rest_framework import serializers

from ..models import ProductCategories, Products


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategories
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Products
        fields = '__all__'
        