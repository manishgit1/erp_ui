from django.views.generic import View
import json
import ast
from django.conf import settings
import requests
from django.http import JsonResponse
from master.globalparamters import get_auth_headers, api_request

API_URL = settings.API_URL



class GeneralSettingsListDataView(View):

   def get(self,request, *args, **kwargs):
      data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))

      setup_type = data['setupType'] if 'setupType' in data else ''

      response = api_request(request,'GET','/master/' +  setup_type + '/lists',data=None,params=None,retries=1)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)


class CheckIfContactExistsView(View):

   def get(self,request, *args, **kwargs):
      # data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      data = request.GET.get('jsonData')
      headers = get_auth_headers(request)

      api_url = API_URL + '/master/contact/checkIfContactExists/'

      response = requests.get(api_url, headers=headers,params={'jsonData': data})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)
      


class AddressInfoView(View):

   def get(self,request, *args, **kwargs):
      # data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      data = request.GET.get('jsonData')
      headers = get_auth_headers(request)

      api_url = API_URL + '/master/vdcMunicipality/getAddressInfo/'

      response = requests.get(api_url, headers=headers,params={'jsonData': data})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)