from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'mobile_no', 'address', 'profile_photo', 'is_staff', 'is_active', 'join_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            mobile_no=validated_data['mobile_no'],
            address=validated_data['address']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all())
    
    class Meta:
        model = Address
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields= '__all__'


class CartSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all())
    items = CartItemSerializer(many=True, read_only=True)
    # user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Cart
        fields = '__all__'
    
