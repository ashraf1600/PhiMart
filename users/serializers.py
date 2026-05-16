from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email', 'password', 'first_name', 'last_name', 'address', 'phone_number']




class UserSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone_number']
        ref_name = 'CustomUser'

