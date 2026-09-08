from django.views.generic import View
from django.conf import settings
import requests
from django.http import JsonResponse
from master.globalparamters import get_auth_headers

API_URL = settings.API_URL


class LoanCollateralTypeListDataView(View):

   def get(self,request,format=None):
      try:
         headers = get_auth_headers(request)
         request_url = API_URL + '/tools/loanCollateralType/list'
         response = requests.get(request_url, timeout=20, headers=headers)
         response.raise_for_status()
         if response.status_code == 200:
           return JsonResponse(response.json(), status=200)
         else:
           return JsonResponse(response.json(), status=500)
      except requests.RequestException as e:
         return JsonResponse({"success": False, "error": str(e)}, status=500)

      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)
