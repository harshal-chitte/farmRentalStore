import json
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session
from django.shortcuts import redirect, render
from django.views import View
from farmer import apiCalls
from rest_framework import status
from django.utils.decorators import method_decorator
from apiApp import models
from farmer.constant import UrlConst
from datetime import datetime
from django.utils import timezone


# Create your views here.
def is_loggedIn(func):
    def wrapper(request, *args, **kwargs):
        
        if request.session.get('user'):
            return func(request, *args, **kwargs)
        else:
            return redirect('login_page')
    return wrapper


class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="login.html", context={})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # get all RentedProductModel entries where to_date is less than current date
        rented_products_to_delete = models.RentedProductModel.objects.filter(to_date__lt=timezone.now())
        # delete all matching entries
        rented_products_to_delete.delete()

        if not username or not password:
            return render(request, template_name="login.html", context={'error':"credentials cannot be empty"})
        
        reqData = {'username':username, 'password':password}
        res = apiCalls.login_api(reqData)
        if res.status_code == status.HTTP_200_OK:
            request.session['refresh_token'] = res.json().get("refresh")
            request.session['access_token'] = res.json().get("access")
            request.session['user'] = {
                "refresh_token":res.json().get("refresh"),
                "access_token":res.json().get("access"),
                "refresh_token":res.json().get("refresh"),
                "is_staff":res.json().get("is_staff"),
                "id":res.json().get("id"),
                "username":res.json().get("username"),
            }
            return redirect('home_page')
        return render(request, template_name="login.html", context={'message':'please enter valid credentials'})
    

class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="register.html", context={})

    def post(self, request, *args, **kwargs):
        req_data = {}
        req_data["username"] = request.POST.get("username")
        req_data["name"] = request.POST.get("name")
        req_data["email"] = request.POST.get("email")
        req_data["password"] = request.POST.get("password")
        req_data["checkpassword"] = request.POST.get("checkpassword")

        if req_data["password"] != req_data["checkpassword"]:
            context = {"error":"password does not match"}
            return render(request, template_name="register.html", context=context)
        
        res = apiCalls.register_api(req_data)
        if res.status_code == status.HTTP_201_CREATED:
            return redirect('login_page')
        return render(request, template_name="register.html", context={})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect('login_page')


@method_decorator(is_loggedIn, name='dispatch')
class HomePageView(View):

    def get(self, request, *args, **kwargs):
        lst = []
        featured_obj = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/product-featured/",
        ).json()
        for itm in featured_obj:
            if itm['p_owner'] != request.session.get("user").get("id") and len(lst) < 3:
                lst.append(itm)
        return render(request, template_name="home.html", context={'nav':'home', 'featured_obj':lst})
    

@method_decorator(is_loggedIn, name='dispatch')
class ShopPageView(View):

    def get(self, request, filter_id=None, *args, **kwargs):
        res_obj = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/product/",
        ).json()
        res_lst = []
        if filter_id:
            for ele in res_obj:
                if ele['p_category'] == filter_id:
                    res_lst.append(ele)
        else:
            res_lst = res_obj
        category_lst_obj = models.ProductCategory.objects.all()
        context = {'data':res_lst, 'category_lst':category_lst_obj}
        if filter_id:
            context['filter'] = models.ProductCategory.objects.get(id=filter_id).category
        
        context['nav']='shop'
        return render(request, template_name="shop.html", context=context)


@method_decorator(is_loggedIn, name='dispatch')
class DetailPageView(View):

    def get(self, request, pk=None, *args, **kwargs):
        res = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/product/{pk}/",
        )
        context = {'data':res.json()}
        context['nav']='shop'
        return render(request, template_name="detail.html", context=context)
    
    def post(self, request, pk=None, *args, **kwargs):
        id = request.POST.get("id")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        now = datetime.now().date()
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
        if from_date_obj < now:
            res = apiCalls.get_api_call(
                url=f"{UrlConst.API_URL.value}/product/{pk}/",
            )
            context = {'data':res.json(), 'error':'Invalid from date'}
            return render(request, template_name="detail.html", context=context)
        elif from_date_obj >= to_date_obj:
            res = apiCalls.get_api_call(
                url=f"{UrlConst.API_URL.value}/product/{pk}/",
            )
            context = {'data':res.json(), 'error':'Invalid from and to date'}
            return render(request, template_name="detail.html", context=context)
        res = apiCalls.post_api_call(
            url=f"{UrlConst.API_URL.value}/raise-rent-request/",
            payload={'prod_id':id, 'renter_id':request.session.get('user').get('id'), 'from_date':from_date, 'to_date':to_date}
        )
        if res.status_code == status.HTTP_201_CREATED:
            context = {'data':res.json(), 'raised':True}
            return render(request, template_name="detail.html", context=context)
        else:
            res = apiCalls.get_api_call(
                url=f"{UrlConst.API_URL.value}/product/{pk}/",
            )
            context = {'data':res.json(), 'error':'request with overlapping timestamp cannot be made for same product.'}
            context['nav']='shop'
            return render(request, template_name="detail.html", context=context)


@method_decorator(is_loggedIn, name='dispatch')
class MyListView(View):

    def get(self, request, *args, **kwargs):
        res = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/my-product/{request.session.get('user').get('id')}/",
        )
        context = {'item_lst':res.json()}
        context['nav']='mylist'
        return render(request, template_name="listed.html", context=context)
    

@method_decorator(is_loggedIn, name='dispatch')
class RaisedRequestView(View):

    def get(self, request, *args, **kwargs):
        res = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/raise-rent-request/{request.session.get('user').get('id')}/renter/",
        )
        context = {'item_lst':res.json()}
        if not res.json():
            context['message']="No requests to Display"
        context['nav']='request'
        return render(request, template_name="raised_request.html", context=context)
    

@method_decorator(is_loggedIn, name='dispatch')
class ReceivedRequestView(View):

    def get(self, request, *args, **kwargs):
        res = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/raise-rent-request/{request.session.get('user').get('id')}/rented/",
        )
        context = {'item_lst':res.json(), 'status':''}
  
        if not res.json():
            context['message']="No requests to Display"
        
        context['nav']='request'
        return render(request, template_name="request_received.html", context=context)


@method_decorator(is_loggedIn, name='dispatch')
class RaisedRequestDetailView(View):

    def get(self, request, prod_id=None, *args, **kwargs):
        res_obj = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/raise-rent-request/{request.session.get('user').get('id')}/renter/",
        )
        res =None
        for itm in res_obj.json():
            if itm['id'] == prod_id:
                res = itm
                break
        from_date = res['from_date']
        to_date = res['to_date']
        from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S%z')
        to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S%z')
        from_date = from_date.date()
        to_date = to_date.date()
        diff = (to_date - from_date).days
        context = {'item_detail':res, 'no_of_days':diff, 'cost':int(diff)*int(res['p_price'])}
        context['nav']='request'
        return render(request, template_name="request_raised_detail.html", context=context)

    def post(self, request, prod_id=None, *args, **kwargs):
        rented_prod_id=request.POST.get("id")
        obj = models.RentedProductModel.objects.get(id=int(rented_prod_id))
        obj.rent_status = 'rented'
        obj.save()
  
        return redirect('raised_request_list_page')

@method_decorator(is_loggedIn, name='dispatch')
class ReceivedRequestDetailView(View):

    def get(self, request, prod_id=None, *args, **kwargs):
        from datetime import datetime
        res = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/rent-detail/{prod_id}/",
        )
        from_date = res.json()[0]['from_date']
        to_date = res.json()[0]['to_date']
        from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S%z')
        to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S%z')
        from_date = from_date.date()
        to_date = to_date.date()

        # calculate difference in days
        diff = (to_date - from_date).days

        context = {'item_detail':res.json()[0], 'no_of_days':diff, 'cost':int(diff)*int(res.json()[0]['p_price'])}

        from apiApp import models
        user_obj = models.User.objects.get(id=res.json()[0]['p_renter'])
        context['username'] = user_obj.username
        context['first_name'] = user_obj.first_name
        context['last_name'] = user_obj.last_name
        context['email'] = user_obj.email
        context['item_detail']['from_date'] = context['item_detail']['from_date'].split('T')[0]
        context['item_detail']['to_date'] = context['item_detail']['to_date'].split('T')[0]
        if context['item_detail']['rent_status'] == 'request_raised':
            context['request_status'] = "Pending"
        elif context['item_detail']['rent_status'] == 'request_accepted':
            context['request_status'] = "Request Accepted"
        elif context['item_detail']['rent_status'] == 'rented':
            context['request_status'] = "Rented Successfully"
        elif context['item_detail']['rent_status'] == 'rejected':
            context['request_status'] = "rejected"
        
        context['nav']='request'
        return render(request, template_name="request_received_detail.html", context=context)
    
    def post(self, request, prod_id=None, *args, **kwargs):
        rented_prod_id=request.POST.get("id")
        obj = models.RentedProductModel.objects.get(id=int(rented_prod_id))
        obj.rent_status = 'request_accepted'
        obj.save()

        return redirect('received_request_detail_page', prod_id=prod_id)


@method_decorator(is_loggedIn, name='dispatch')
class AddProductView(View):
    def get(self, request, *args, **kwargs):
        category_lst = models.ProductCategory.objects.all()
        context = {'category_lst':category_lst}
        return render(request, template_name="additem.html", context=context)
    
    def post(self, request, *args, **kwargs):
        req_data={
            'p_owner':request.session.get('user').get('id'),
            'p_name':request.POST.get("p_name"),
            'p_desc':request.POST.get("p_desc"),
            'p_price':request.POST.get("p_price"),
            'r_status':False,
            'p_category':request.POST.get("category"),
        }
        res = apiCalls.post_api_call(
            url=f"{UrlConst.API_URL.value}/product/",
            payload=req_data,
            files={"p_img": request.FILES.get("p_img")},
        )
        if res.status_code == status.HTTP_201_CREATED:
            return redirect("list_page")
        
        context = {"error":"Something went wrong"}
        return render(request, template_name="additem.html", context=context)


@method_decorator(is_loggedIn, name='dispatch')
class UpdateProductView(View):
    def get(self, request, id=None, *args, **kwargs):
        res = apiCalls.get_api_call(
            url=f"{UrlConst.API_URL.value}/product/{id}/",
        )
        context = {'data':res.json(), 'type':'update'}
        return render(request, template_name="additem.html", context=context)
    
    def post(self, request, *args, **kwargs):
        req_data={
            'id':request.POST.get("id"),
            'p_name':request.POST.get("p_name"),
            'p_desc':request.POST.get("p_desc"),
            'p_price':request.POST.get("p_price"),
        }

        if 'delete_btn' in request.POST:
            models.ProductModel.objects.get(id=request.POST.get("id")).delete()
            return redirect("list_page")

        res = apiCalls.put_api_call(
            url=f"{UrlConst.API_URL.value}/product/{request.POST.get('id')}/",
            payload=req_data,
            files={"p_img": request.FILES.get("p_img")},
        )
        if res.status_code == status.HTTP_200_OK:
            return redirect("list_page")
        
        context = {"error":"Something went wrong"}
        return render(request, template_name="additem.html", context=context)
    

@method_decorator(is_loggedIn, name='dispatch')
class RentedProductView(View):

    def get(self, request, *args, **kwargs):
        
        return render(request, template_name="rented.html")


@method_decorator(is_loggedIn, name='dispatch')
class CheckOutView(View):

    def get(self, request, *args, **kwargs):
        return render(request, template_name="checkout.html")