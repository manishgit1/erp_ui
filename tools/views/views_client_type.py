from django.views.generic import View
from django.shortcuts import render
import json
import ast
from django.conf import settings
from django.http import JsonResponse
import requests
from master.globalparamters import get_auth_headers, api_request


API_URL = settings.API_URL

class ClientTypeListView(View):
  
  def get(self,request,format=None):
    return render(request,'tools/client_type/client_type_list.html')
  



class ClientTypeCreateView(View):
  
  def get(self,request,format=None):
    setup_type = request.GET.get('setupType')
    data = {}
    if setup_type:
        data['setupType'] = setup_type

    context = {
        'data': json.dumps(data)
    }
    return render(request,'tools/client_type/client_type_create.html',context=context)
  

  def post(self,request,*args):
      try:
         # headers = {
         #    "Content-Type": request.META.get("CONTENT_TYPE", "application/json")
         # }

         data = json.loads(request.GET.get('jsonData'))

         setup_type  = str(data['setupType']).strip() if 'setupType' in data else ''
         headers = get_auth_headers(request)

         request_url = API_URL + '/tools/' + setup_type + '/create'
         response = requests.post(
               request_url,
               data=request.body,
               headers=headers,
               timeout=30
         )

         response = api_request()

         if response.status_code == 200:
           return JsonResponse(response.json(), status=200)
         else:
           try:
               return JsonResponse(response.json(), status=500)
           except ValueError:
               return JsonResponse({'status': 'error', 'message': 'Invalid response from API', 'content': response.text}, status=500)

      except requests.exceptions.Timeout:
         return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)

      except requests.exceptions.RequestException as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=502)

      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)


class ClientTypeListDataView(View):

   def get(self,request, *args, **kwargs):
      try:
          data = json.loads(request.GET.get('jsonData'))
      except json.JSONDecodeError:
          return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
      # headers = {
      #           'Authorization': request.session.get('authdata'),
      #           'Temp-Session-Id': request.session.get('temp_session_id')
      # }

      setup_type = data['setupType'] if 'setupType' in data else ''
      api_url = API_URL + '/tools/' +  setup_type + '/list'
      
      try:

          response = api_request(request, 'GET', '/tools/' + setup_type + '/list', data=None, params=None, retries=1)
        #   headers = get_auth_headers(request)
        #   response = requests.get(api_url, headers=headers)
      except requests.exceptions.RequestException as e:
          return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         try:
             return JsonResponse(response.json(), status=500)
         except ValueError:
             return JsonResponse({'status': 'error', 'message': 'Invalid response from API', 'content': response.text}, status=500)