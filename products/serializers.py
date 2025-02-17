from rest_framework import serializers
from .models import Product
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


class ProductsListSerializer(TaggitSerializer, serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ('name', 'slug', 'tags', 'sku', 'price',
                  'image_thumbnail', 'created_at', 'updated_at', 'is_published', 'is_delete', 'avg_rating', 'category',) 
        
