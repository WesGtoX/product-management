import random

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from producer import publish
from products.models import Product, User
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        publish('product_deleted', dict(pk=pk))
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):

    def post(self, response):
        user = User.objects.create()
        return Response(dict(id=user.id, message='User registered successfully'))

    def get(self, response):
        users = User.objects.all()

        if users.count() > 0:
            user = random.choice(users)
            return Response(dict(id=user.id))

        return Response(dict(message='No registered user'))
