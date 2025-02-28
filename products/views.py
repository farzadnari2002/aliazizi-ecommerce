from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.serializers import ProductsListSerializer, ProductDetailSerializer, CategorySerializer, FavoriteProductSerializer
from rest_framework.permissions import IsAuthenticated
from products.models import Product, CategoryProduct, FavoriteProduct
from django.shortcuts import get_list_or_404
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator



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


@method_decorator(ratelimit(key='user', rate='5/m', method='POST', block=True), name='dispatch')
class FavoriteProductView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteProductSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            product = get_list_or_404(Product, slug=data['product_slug'], is_published=True, is_delete=False)

            like, created = FavoriteProduct.objects.get_or_create(user=request.user, product_id=product[0].id)  

            if created:
                action = 'liked'
            else:
                like.delete()
                action = 'unliked'

            return Response({"message": f"You have {action} this product."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
