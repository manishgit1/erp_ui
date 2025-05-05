from django.shortcuts import render
from django.views.generic import View
from django.conf import settings

import requests
from django.http.response import JsonResponse
import json
# Create your views here.
import ast

API_URL = settings.API_BASE_URL

class ContactMasterCreateView(View):
   
   def get(self,request):
      return render(request,'master/contact_master.html')
   
   def post(self,request,*args,**kwargs):
      data = json.loads(request.body)

      headers = {
                'Authorization': request.session.get('authdata'),
                'Temp-Session-Id': request.session.get('temp_session_id')
      }
      api_url = API_URL + '/contact/create'

      response = requests.post(api_url, json=data, headers=headers)
      if response.status_code == '200':
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)
   

class GeneralSettingsView(View):
   def get(self,request):
      return render(request, 'master/settings_create.html')
   
   def post(self,request, *args, **kwargs):
      data = json.loads(request.body)

      headers = {
                'Authorization': request.session.get('authdata'),
                'Temp-Session-Id': request.session.get('temp_session_id')
      }

      setup_type = data['setupType'] if 'setupType' in data else  ''
      api_url = API_URL + '/' + setup_type + '/create'

      response = requests.post(api_url, json=data, headers=headers)

      if response.status_code == '200':
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)
      

class GeneralSettingsListDataView(View):

   def get(self,request, *args, **kwargs):
      data = ast.literal_eval(json.dumps(json.loads(request.GET.get('jsonData'))))
      headers = {
                'Authorization': request.session.get('authdata'),
                'Temp-Session-Id': request.session.get('temp_session_id')
      }

      setup_type = data['setupType'] if 'setupType' in data else ''
      api_url = API_URL + '/' +  setup_type + '/lists'

      response = requests.get(api_url, headers=headers)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)




   
class GeneralSettingsCreateView(View):
   def get(self,request):
      return render(request, 'master/settings_create.html')
   
   