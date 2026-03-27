from django.views.generic import CreateView, View
from django.shortcuts import render
from django.conf import settings
import requests
from django.http import JsonResponse
from master.globalparamters import get_auth_headers

API_URL = settings.API_URL


class LoanTypeCreateView(CreateView):
   
   def get(self,request,format=None):
      return render(request, 'tools/loan_type/loan_type_create.html')
   

   def post(self,request,*args):
      try:
         headers = get_auth_headers(request)

         response = requests.post(
               API_URL + '/tools/loanType/create',
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
      

class LoanTypeListView(View):

   def get(self,request,format=None):
      return render(request, 'tools/loan_type/loan_type_list.html')



class LoanTypeListDataView(View):

   def get(self,request,format=None):
      try:
         headers = get_auth_headers(request)
         request_url = API_URL + '/tools/loanType/list'
         response = requests.get(request_url, timeout=20, headers=headers)
         response.raise_for_status()  
         if response.status_code == 200:
            return JsonResponse(response.json(), status=200)
         else:
            return JsonResponse(response.json(), status=500)
      except requests.RequestException as e:
         return JsonResponse({"success": False, "error": str(e)}, status=500)
      
      except requests.HTTPError as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)
      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)