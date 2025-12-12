from django.views.generic import View
from django.shortcuts import render
import json
import ast
from django.conf import settings
from django.http import JsonResponse
import requests


API_URL = settings.API_URL

class ClientTypeListView(View):
  
  def get(self,request,format=None):
    return render(request,'tools/client_type/client_type_list.html')
  



class ClientTypeCreateView(View):
  
  def get(self,request,format=None):
     return render(request,'tools/client_type/client_type_create.html')
  

  def post(self,request,*args):
      try:
         # headers = {
         #    "Content-Type": request.META.get("CONTENT_TYPE", "application/json")
         # }

         data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))

         setup_type  = str(data['setupType']).strip() if 'setupType' in data else ''
      # headers = {
         headers = {
            'Content-Type': request.META.get("CONTENT_TYPE", "application/json"),
            'Authorization': request.session.get('authdata'),
            'Temp-Session-Id': request.session.get('temp_session_id')
         }

         request_url = API_URL + '/tools/' + setup_type + '/create'
         response = requests.post(
               request_url,
               data=request.body,
               headers=headers,
               timeout=30
         )

         if response.status_code == 200:
           return JsonResponse(response.json(), status=200)
         else:
           return JsonResponse(response.json(), status=500)

      except requests.exceptions.Timeout:
         return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)

      except requests.exceptions.RequestException as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=502)

      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)


class ClientTypeListDataView(View):

   def get(self,request, *args, **kwargs):
      data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      # headers = {
      #           'Authorization': request.session.get('authdata'),
      #           'Temp-Session-Id': request.session.get('temp_session_id')
      # }

      setup_type = data['setupType'] if 'setupType' in data else ''
      api_url = API_URL + '/tools/' +  setup_type + '/list'

      print(api_url)

      response = requests.get(api_url, headers={})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)