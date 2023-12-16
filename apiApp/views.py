from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from rest_framework.response import Response
from apiApp import models, serializers
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from apiApp.serializers import getJWTTokenSerializer, UserSerializerWithToken
from apiApp import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class userLoginView(TokenObtainPairView):
    serializer_class = getJWTTokenSerializer


# user registration view
@api_view(["POST"])
def registerView(request):
    data = request.data
    if data["password"] != data["checkpassword"]:
        print("ehererere i amma")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if data["name"] and len(data["name"].split(" ")) == 2:
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"].split(" ")[0],
            last_name = data["name"].split(" ")[1],
            password=make_password(data["password"]),
        )
    elif data["name"] and len(data["name"].split(" ")) >2:
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"].split(" ")[-1],
            last_name = data["name"].split(" ")[0],
            password=make_password(data["password"]),
        )
    else:    
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"],
            password=make_password(data["password"]),
        )
    serialized_data = UserSerializerWithToken(user_obj, many=False)
    if serialized_data.is_valid:
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)
    else:
        print(serialized_data.errors)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListedApi(mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = models.ProductModel.objects.all().order_by('-id')
    serializer_class = serializers.ProductModelSerializer

    def get(self, request, pk=None, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ProductApi(mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductModelSerializer

    def create(self, request, req_data, *args, **kwargs):
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, req_data, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=req_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            self.serializer_class = serializers.CustomProductModelSerializer
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def put(self, request, pk=None, *args, **kwargs):
        req_data = request.data.copy()
        prod_obj = models.ProductModel.objects.get(id=req_data.get('id'))

        req_data['p_img'] = request.FILES.get("p_img")
        if not req_data.get('p_img'):
            req_data['p_img'] = prod_obj.p_img
        return self.update(request, req_data, *args, **kwargs, files=request.FILES)
    
    def post(self, request, *args, **kwargs):
        req_data = request.data.copy()
        req_data['p_img'] = request.FILES.get("p_img")
        return self.create(request, req_data, *args, **kwargs, files=request.FILES)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MyProductApi(mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductModelSerializer

    def get(self, request, pk=None, *args, **kwargs):
        self.queryset = models.ProductModel.objects.filter(p_owner__id=pk)
        return self.list(request, *args, **kwargs)


class MyProductFilterApi(mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductModelSerializer

    def get(self, request, pk=None, *args, **kwargs):
        self.queryset = models.ProductModel.objects.filter(p_category=pk)
        return self.list(request, *args, **kwargs)


class RentedProductView(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    ):

    queryset = models.RentedProductModel.objects.all()
    serializer_class = serializers.RentedProductModelSerializer

    def create(self, request, req_data, *args, **kwargs):
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get(self, request, pk=None, type=None, *args, **kwargs):
        if type == 'renter':
            self.queryset = models.RentedProductModel.objects.filter(p_renter__id=pk)
        else:
            self.queryset = models.RentedProductModel.objects.filter(p_owner__id=pk)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        prod_id = request.POST.get("prod_id")
        renter_id = request.POST.get("renter_id")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        proj_obj = models.ProductModel.objects.get(id=prod_id)

        req_data={
            'p_owner':proj_obj.p_owner.id,
            'p_renter':renter_id,
            'product':prod_id,
            'p_name':proj_obj.p_name,
            'p_desc':proj_obj.p_desc,
            'p_img':proj_obj.p_img,
            'p_price':proj_obj.p_price,
            'r_status':False,
            'p_category':proj_obj.p_category,
            'from_date':from_date,
            'to_date':to_date
        }
        return self.create(request, req_data, *args, **kwargs, files=request.FILES)
    
    def put(self, request, pk=None, *args, **kwargs):
        proj_obj = models.ProductModel.objects.get(id=pk)
        proj_obj.r_status = True
        proj_obj.save()
        return Response(status=status.HTTP_200_OK)



class RentedProductByIDView(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    ):

    queryset = models.RentedProductModel.objects.all()
    serializer_class = serializers.RentedProductModelSerializer

    def get(self, request, pk=None, type=None, *args, **kwargs):
        self.queryset = models.RentedProductModel.objects.filter(id=pk)
        return self.list(request, *args, **kwargs)
# import datetime
# class RentApprovedApi(
#     generics.GenericAPIView,
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin):

#     def create(self, request, req_data, *args, **kwargs):
#         serializer = self.get_serializer(data=req_data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
#     def post(self, request, *args, **kwargs):
#         product_id = request.POST.get("prod_id")
#         prod_obj = models.RentedProductModel.objects.get(id=product_id)
#         p_owner = prod_obj.p_owner
#         p_renter = prod_obj.p_renter

#         num_days = int(request.POST.get('num_days'))
#         current_date_time = datetime.datetime.now()
#         from_date_time = current_date_time + datetime.timedelta(hours=24)
#         to_date_time = from_date_time + datetime.timedelta(days=num_days)
#         req_data={
#             'from_date_time':from_date_time,
#             'to_date_time':to_date_time,
#             'r_product':product_id,
#             'p_owner':p_owner,
#             'p_renter':p_renter,
#         }
#         return self.create(request, req_data, *args, **kwargs)


# class RentRelationApi(
#     generics.GenericAPIView,
#     mixins.RetrieveModelMixin,
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin):

#     queryset = models.RentedProductModel.objects.all()
#     serializer_class = serializers.RentalRelationSerializer

#     def get(self, request, prod_id=None, renter_id=None, type=None, *args, **kwargs):
#         if type == 'owner':
#             obj = models.RentedProductModel.objects.filter(
#                 id=prod_id,
#                 p_owner = renter_id
#             ).first()
#             self.serializer_class = serializers.RentalOwnerRelationSerializer
#         else:
#             obj = models.RentedProductModel.objects.filter(
#                 id=prod_id,
#                 p_renter = renter_id
#             ).first()
        
#         obj_dict = model_to_dict(obj)
#         serialized_data = self.serializer_class(data=obj_dict).data
#         return Response(status=status.HTTP_200_OK, data={'data':serialized_data})


# class RentReceivedReqRelationApi(
#     generics.GenericAPIView,
#     mixins.RetrieveModelMixin,
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin):

#     queryset = models.RentedProductModel.objects.all()
#     serializer_class = serializers.RentalRelationSerializer

#     def get(self, request, prod_id=None, p_owner=None, *args, **kwargs):
#         obj = models.RentedProductModel.objects.filter(
#             product=prod_id,
#             p_owner=p_owner
#         ).first()
#         return Response(status=status.HTTP_200_OK)