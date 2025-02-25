from rest_framework import serializers
from .models import (
    Product,
    CategoryProduct,
    ColorProduct,
    ImagesProduct,
    SpecificationsProduct,
    CommentProduct,
)

# Serializers for Images
class ImagesProductSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = ImagesProduct
        fields = ('image', 'image_thumbnail')
        read_only_fields = ('image', 'image_thumbnail')

# Serializers for Product Details
class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('name', 'slug')

class ColorProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorProduct
        fields = ('name', 'color_code')

class SpecificationsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationsProduct
        fields = ('title', 'desc')

# Serializers for Comments
class CommentProductSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user.mask_contact_info', read_only=True)
    avatar_thumbnail = serializers.ImageField(source='user.userprofile.avatar_thumbnail', read_only=True)

    class Meta:
        model = CommentProduct
        fields = ('username', 'rating', 'comment', 'avatar_thumbnail', 'count_rating')

# Serializers for Product Listings
class ProductsListSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'slug', 'price', 'image_thumbnail', 'avg_rating')

# Serializer for Product Detail
class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer()
    color = ColorProductSerializer(many=True)
    size = serializers.StringRelatedField(many=True)
    images = ImagesProductSerializer(many=True)
    specifications = SpecificationsProductSerializer(many=True)
    comments = CommentProductSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'price', 'image',
            'short_desc', 'description', 'category',
            'color', 'size', 'avg_rating',
            'images', 'specifications', 'comments'
        )


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    parent = serializers.StringRelatedField()
    parent_id = serializers.IntegerField(required=False)
    class Meta:
        model = CategoryProduct
        fields = ('children', 'name', 'slug', 'parent', 'parent_id')
