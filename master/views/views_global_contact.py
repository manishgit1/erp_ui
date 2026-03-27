from django.views.generic import CreateView, View
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
from master.globalparamters import get_auth_headers
import json
import ast

API_URL = settings.API_URL

class GlobalContactCreateView(CreateView):
   def get(self,request, format=None):
      return render(request, 'master/global_contact/contact_master_create.html')
   

   def post(self,request,*args):
      try:
         headers = get_auth_headers(request)

         response = requests.post(
               API_URL + '/master/contactMaster/create',
               data=request.body,
               headers=headers,
               timeout=30
         )

         return JsonResponse(response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text, status=response.status_code)

      except requests.exceptions.Timeout:
         return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)

      except requests.exceptions.RequestException as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=502)

      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)

class GlobalContactListView(View):
   
   def get(self,request,format=None):
      return render(request, 'master/global_contact/contact_master_list.html')
   


class GlobalContactListDataView(View):

   def get(self,request, *args, **kwargs):
      headers = get_auth_headers(request)

      api_url = API_URL + '/master/contactMaster/list'

      response = requests.get(api_url, headers=headers)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)
      


class GlobalContactEditView(View):
   def get(self,request,pk, format=None):
      context = {
         'contactId': pk
      }

      return render(request, 'master/global_contact/contact_master_update.html', context=context) 
   
   def post(self,request,pk,format=None):
      try:
         headers = get_auth_headers(request)
         
         request_url = API_URL + '/master/contactMaster/' + pk + '/edit'

         response = requests.post(
               request_url,
               data=request.body,
               headers=headers,
               timeout=30
         )

         return JsonResponse(response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text, status=response.status_code)

      except requests.exceptions.Timeout:
         return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)

      except requests.exceptions.RequestException as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=502)

      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)

   



class GlobalContactDataByIdView(View):

   def get(self,request,pk,format=None):
      headers = get_auth_headers(request)

      api_url = API_URL + '/master/contactMaster/'+ pk + '/findById'

      response = requests.get(api_url, headers=headers)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)


class GetAddressByMunicipalityView(View):

   def get(self,request,format=None):
      data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      # data = request.GET.get('jsonData')
      headers = get_auth_headers(request)

      api_url = API_URL + '/master/vdcMunicipality/getAddressInfo/'

      response = requests.get(api_url, headers=headers,params={'jsonData': json.dumps(data)})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)
