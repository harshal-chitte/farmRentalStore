from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from farmer import views

urlpatterns = [
    path('user-login/', views.UserLoginView.as_view(), name='login_page'),
    path('', views.UserLoginView.as_view(), name='login_page'),
    path('user-logout/', views.LogoutView.as_view(), name='logout_page'),
    path('users/register/', views.UserRegisterView.as_view(), name='user_register'),
    path('home/', views.HomePageView.as_view(), name='home_page'),
    path('shop/', views.ShopPageView.as_view(), name='shop_page'),
    path('shop/<int:filter_id>/', views.ShopPageView.as_view(), name='filter_shop_page'),
    path('shop-detail/<int:pk>/', views.DetailPageView.as_view(), name='shop_detail_page'),
    
    path('my-list/', views.MyListView.as_view(), name='list_page'),
    path('add-item/', views.AddProductView.as_view(), name='add_item_page'),
    path('update-item/<int:id>/', views.UpdateProductView.as_view(), name='update_item_page'),
    path('rented/', views.RentedProductView.as_view(), name='rented_page'),
    path('checkout/', views.CheckOutView.as_view(), name='checkout_page'),
    path('raised-request-list/', views.RaisedRequestView.as_view(), name='raised_request_list_page'),
    path('received-request-list/', views.ReceivedRequestView.as_view(), name='received_request_list_page'),
    path('raised-request-detail/<int:prod_id>/', views.RaisedRequestDetailView.as_view(), name='raised_request_detail_page'),
    path('received-request-detail/<int:prod_id>/', views.ReceivedRequestDetailView.as_view(), name='received_request_detail_page'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
