from rest_framework import serializers
from .models import Product


class ProductsListSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'slug', 'price', 'image_thumbnail', 'avg_rating') 
