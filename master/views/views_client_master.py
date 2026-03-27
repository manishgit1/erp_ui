from django.views.generic import CreateView, View
from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.conf import settings
from master.globalparamters import get_auth_headers
import json
import ast
import logging


logger = logging.getLogger('erp_ui')

API_URL = settings.API_URL

class ClientMasterListView(View):
   
   def get(self,request,format=None):
      return render(request, 'master/client_master/client_master_list.html')


class ClientMasterCreateView(View):
   
   def get(self,request,format=None):

      raw_data = request.GET.get('jsonData')
      data = {}
      if raw_data:
         try:
            data = ast.literal_eval(raw_data)
            if not isinstance(data, dict):
               data = {}
         except (ValueError, SyntaxError):
            data = {}

      context = {
         'data': json.dumps(data)
      }
      return render(request, 'master/client_master/client_master_create.html',context)
   

   def post(self,request,*args):
      try:
         headers = get_auth_headers(request)

         response = requests.post(
               API_URL + '/master/clientMaster/create',
               data=request.body,
               headers=headers,
               timeout=30
         )

         return JsonResponse({
               "status": "success" if response.ok else "error",
               "status_code": response.status_code,
               "response": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
         }, status=response.status_code)

      except requests.exceptions.Timeout:
         return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)

      except requests.exceptions.RequestException as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=502)

      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)
      
class ClientMasterListDataView(View):

   def get(self,request, *args, **kwargs):
      headers = get_auth_headers(request)

      api_url = API_URL + '/master/clientMaster/list'

      response = requests.get(api_url, headers=headers)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)

class ClientMasterCheckIfClientExistsView(View):

   def get(self,request, *args, **kwargs):

      data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      headers = get_auth_headers(request)

      api_url = API_URL + '/master/clientMaster/checkIfClientExists/'
      logger.info(data,exc_info=True)

      response = requests.get(api_url, headers=headers,params={'jsonData': json.dumps(data)})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)


class ClientMasterUpdateView(View):
   def get(self,request,pk,format=None):
      context = {
         'clientId': pk
      }
      return render(request, 'master/client_master/client_master_update.html',context)

class ClientMasterDataByIdView(View):
   def get(self,request,pk,format=None):
      api_url = API_URL + '/master/clientMaster/' + str(pk) + '/findById'
      headers = get_auth_headers(request)
      response = requests.get(api_url, headers=headers)
      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)

class ClientMasterEditView(View):
    def post(self,request,pk,format=None):
          headers = get_auth_headers(request)
          response = requests.post(
                API_URL + '/master/clientMaster/' + str(pk) + '/edit',
                data=request.body,
                headers=headers,
                timeout=30
          )
          return JsonResponse({
                "status": "success" if response.ok else "error",
                "status_code": response.status_code,
                "response": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
          }, status=response.status_code)



class ClientMasterGetLeadDataView(View):

   def get(self,request, *args, **kwargs):

      data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      headers = get_auth_headers(request)

      api_url = API_URL + '/master/clientMaster/getLeadData/'

      response = requests.get(api_url, headers=headers,params={'jsonData': json.dumps(data)})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)