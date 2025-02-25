from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.serializers import ProductsListSerializer, ProductDetailSerializer, CategorySerializer
from products.models import Product, CategoryProduct
from django.shortcuts import get_list_or_404


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
