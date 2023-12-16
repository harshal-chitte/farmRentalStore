from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apiApp import views

urlpatterns = [
    path('users/login/', views.userLoginView.as_view(), name='token_obtain_pair'),
    path('users/register/', views.registerView, name='register'),
    
    path('product/', views.ProductApi.as_view(), name='product_api_page'),
    path('product-featured/', views.ProductListedApi.as_view(), name='product_featured'),
    path('product/<int:pk>/', views.ProductApi.as_view(), name='product_api_page'),
    path('my-product/<int:pk>/', views.MyProductApi.as_view(), name='my_product_api_page'),
    path('raise-rent-request/', views.RentedProductView.as_view(), name='raise_rent_request'),
    path('raise-rent-request/<int:pk>/<str:type>/', views.RentedProductView.as_view(), name='raise_rent_request'),
    path('rent-detail/<int:pk>/', views.RentedProductByIDView.as_view(), name='rent_detail'),
    path('filter-list/<int:pk>/', views.MyProductFilterApi.as_view(), name='filter_list'),
    
    # path('approve-rent-request/', views.RentApprovedApi.as_view(), name='approve_raise_rent_request'),
    # path('rent-detail/<int:prod_id>/<int:renter_id>/<str:type>/', views.RentRelationApi.as_view(), name='rent_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
