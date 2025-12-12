from django.views.generic import CreateView, View
from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.conf import settings
import json
import ast


API_URL = settings.API_URL

class ClientMasterListView(View):
   
   def get(self,request,format=None):
      return render(request, 'master/client_master/client_master_list.html')
   


class ClientMasterCreateView(View):
   
   def get(self,request,format=None):

      json_data = json.dumps(ast.literal_eval(request.GET.get('jsonData')))

      if json_data:
         try:
            data = json.loads(json_data)
         except json.JSONDecodeError as e:
            data = {}
      else:
         data = {}
      context = {
         'data': json.dumps(data)
      }
      return render(request, 'master/client_master/client_master_create.html',context)
   

   def post(self,request,*args):
      try:

         print('client master create')
         headers = {
               "Content-Type": request.META.get("CONTENT_TYPE", "application/json")
         }
         # if "Authorization" in request.headers:
         #       headers["Authorization"] = request.headers["Authorization"]

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
      


class ClientMasterCheckIfClientExistsView(View):

   def get(self,request, *args, **kwargs):
      data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      # data = request.GET.get('jsonData')
      headers = {
               #  'Authorization': request.session.get('authdata'),
               #  'Temp-Session-Id': request.session.get('temp_session_id')
      }

      api_url = API_URL + '/master/clientMaster/checkIfClientExists/'

      response = requests.get(api_url, headers=headers,params={'jsonData': json.dumps(data)})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)