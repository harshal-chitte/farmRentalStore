from rest_framework import serializers
from apiApp import models
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'password']
        # write_only_fields = ['password']
    
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name


class getJWTTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except Exception as e:
            print(e)
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["is_staff"] = self.user.is_staff
        data["id"] = self.user.id

        return data


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])   
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'token', 'password']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductModel
        fields = '__all__'


class CustomProductModelSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductModel
        fields = ['id', 'p_owner', 'p_name', 'p_desc', 'p_img', 'p_price', 'r_status', 'p_category', 'category_name']

    def get_category_name(self, obj):
        return obj.p_category.category


class RentedProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RentedProductModel
        fields = '__all__'


class RentedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RentedProductModel
        fields = ('id', 'p_name', 'p_desc', 'p_img', 'p_price')


