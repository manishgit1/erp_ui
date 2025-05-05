from django.shortcuts import render
from django.views.generic import CreateView, ListView
from globalparameters.views import validate_create_post_request
from django.conf import settings
from django.http import JsonResponse
import requests
import json


# Create your views here.


API_BASE_URL = settings.API_BASE_URL
class OrderCreateView(CreateView):

    def post(self,request, *args, **kwargs):
       request_url = API_BASE_URL + "orders/create"

       try:
            data = json.loads(request.body)
            print(data)
            headers = {
                'Authorization': request.session.get('authdata'),
                'Temp-Session-Id': request.session.get('temp_session_id')
            }

            response = requests.post(request_url,data=json.dumps(data),headers=headers)
            print(response)
            if response.status_code == 200:
                success_message = {
                    'resultCode': '0',
                    'resultDescription': 'Order Created Successfully'
                }
                return JsonResponse(success_message, status=200)
            
            else:
                error = {
                    'resultCode': '-100',
                    'resultDescription': 'Something Went Wrong'
                }
                return JsonResponse(error, status=500)
    
       except Exception as e:
          error = {
            'resultCode': '-104',
            'resultDescription': 'Internal Server Error'
           }
          return JsonResponse(error, status=500)
       

class OrderListGetView(ListView):

    def get(self,request,  *args, **kwargs):

        # if request.session.get('isAdmin'):
        #     return render(request, 'orders/view_orders_admin.html')
        return render(request, 'orders/my_orders.html')


class OrderListGetDataView(ListView):

    def get(self, request, *args, **kwargs):
        request_url = API_BASE_URL + "orders/lists/"

        try:
            headers = {
                'Authorization': request.session.get('authdata'),
                'Temp-Session-Id': request.session.get('temp_session_id')
            }

            response = requests.get(request_url, headers=headers)
            print(response)
            if response.status_code == 200:
                orders = response.json()
                return JsonResponse(orders, status=200)
            
            else:
                error = {
                    'resultCode': '-100',
                    'resultDescription': 'Something Went Wrong'
                }
                return JsonResponse(error, status=response.status_code)
    
        except Exception as e:
            error = {
                'resultCode': '-104',
                'resultDescription': 'Internal Server Error'
            }
            return JsonResponse(error, status=500)