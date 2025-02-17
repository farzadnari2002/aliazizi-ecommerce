from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.serializers import ProductsListSerializer
from products.models import Product  


class ProductsListView(APIView):
    serializer_class = ProductsListSerializer

    def get(self, request):
        products = Product.objects.filter(is_published=True, is_delete=False, id=1)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
