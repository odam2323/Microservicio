from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from .producer import publish
import random


class ProductViewSet(viewsets.ModelViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
    
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_created', serializer.data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_updated', serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def destroy (self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=204)
    
class UserAPIView(APIView):
    def get(self, _):
        user = user.object.all()
        user = random.choice(user)
        return Response ({
            'id': user.id
            })
                          
                          