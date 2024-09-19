from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .serializers import *
from .models import *
from book.models import Review

class UserViewSet(viewsets.ViewSet):
    # queryset = User.objects.all()
    permission_classes = [AllowAny]
    
    @extend_schema(request=UserSerializer)
    @action(detail=False, methods=['POST'])
    def sign_up(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(request=LoginSerializer)
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class AddressViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    
    def get_queryset(self):

        return Address.objects.filter(user=self.request.user)
    
    def get_object(self, pk):

        try:
            address = Address.objects.get(pk=pk,user= self.request.user)
        except Address.DoesNotExist:
             raise("You do not have permission to access this address.")
        
        return address

    @extend_schema(request=AddressSerializer)
    def create(self, request):

        serializer = AddressSerializer(data=request.data)
        
        if(serializer.is_valid()):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):

        try:
            address = self.get_object().get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error':'address Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def update(self, request, pk=None):
        try:
            address = Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return Response({'error':'address Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        try:
            address = Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return Response({'error':'Address Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


    def list(self, request):
        serializer = CartItemSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(request=CartSerializer)
    def create(self,  request):
        serializer = CartSerializer(request.data)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=CartSerializer)
    def retrieve(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'error':'Cart Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(request=CartSerializer)
    def update(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'error':'Cart Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'error':'Cart Not Found'}, status=status.HTTP_404_NOT_FOUND)

        cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    # def list(self, request):

    # def create(self,  request):

    # def retrieve(self, request):

    # def update(self, request):
    
    # def destroy(self, request):
    