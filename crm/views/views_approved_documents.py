from django.views.generic import CreateView, View, ListView
from django.shortcuts import render
import requests
from django.conf import settings
import logging
from django.http import JsonResponse
from master.globalparamters import get_auth_headers
from master.globalparamters import api_request
API_URL = settings.API_URL
import json
import ast

logger = logging.getLogger('erp_ui')


class ApprovedDocumentsListView(View):
   
   def get(self,request,format=None):
      return render(request, 'crm/approved_documents/approved_documents.html')
   

class ApprovedDocumentsListDataView(View):

   def get(self,request, *args, **kwargs):
      # headers = get_auth_headers(request)
      response = api_request(request,'GET','/crm/approvedDocuments/list',data=None)
      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)
      


class DocumentApprovalApproveRejectDocumentsView(View):
   
    def post(self,request,*args,**kwargs):
      try:
         headers = get_auth_headers(request)

         response = requests.post(
               API_URL + '/crm/documentApproval/rejectApprove/create',
               data=request.body,
               headers=headers,
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