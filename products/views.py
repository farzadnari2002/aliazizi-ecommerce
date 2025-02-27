from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from products.serializers import ProductsListSerializer, ProductDetailSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from products.models import Product, CategoryProduct, LikeProduct
from django.shortcuts import get_list_or_404
from django.core.cache import cache
from django.utils import timezone


class ProductsListView(APIView):
    serializer_class = ProductsListSerializer

    def get(self, request):
        products = Product.objects.filter(is_published=True, is_delete=False)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    serializer_class = ProductDetailSerializer

    def get(self, request, slug):
        product = get_list_or_404(Product, slug=slug, is_published=True, is_delete=False)
        serializer = self.serializer_class(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesListView(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        category = CategoryProduct.objects.all()
        serializer = self.serializer_class(category, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeProductView(ViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'product_slug'

    def like_product(self, request, product_slug):
        try:
            product = Product.objects.get(slug=product_slug, is_published=True, is_delete=False)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        cooldown_time = 10
        user_key = f"like_cooldown_{request.user.id}_{product.id}"
        last_action_time = cache.get(user_key)

        if last_action_time and (timezone.now() - last_action_time).seconds < cooldown_time:
            return Response({'error': 'Please wait before liking again.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        like, created = product.likes.get_or_create(user=request.user)  

        if created:
            action = 'liked'
        else:
            like.delete()
            action = 'unliked'
        
        cache.set(user_key, timezone.now(), timeout=cooldown_time)
        return Response({"message": f"You have {action} this product."}, status=status.HTTP_200_OK)
