from django.views.generic import View
from django.shortcuts import render
import requests
from django.http import JsonResponse
import logging
from django.conf import settings
from master.globalparamters import get_auth_headers

logger = logging.getLogger('erp_ui')
API_URL = settings.API_URL

class DocumentUploadCreateView(View):
   
   def get(self,request,format=None):
     lead_id = request.GET.get('leadId')
     print(lead_id)
     context  = {
        'leadId': lead_id
     }
     return render(request, 'crm/document_upload/document_upload.html',context=context)
   
   def post(self,request,*args,**kwargs):
      try:
         headers = get_auth_headers(request)

         response = requests.post(
               API_URL + '/crm/documentUpload/create',
               data=request.body,
               headers=headers,
               # timeout=30
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


class DocumentUploadUploadView(View):
   
   def post(self,request,*args,**kwargs):
      try:
         headers = get_auth_headers(request)

         response = requests.post(
               API_URL + '/crm/documentUpload/upload',
               data=request.body,
               headers=headers,
               # timeout=30
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