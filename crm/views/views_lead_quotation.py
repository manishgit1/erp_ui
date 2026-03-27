from django.views.generic import CreateView, View, ListView
from django.shortcuts import render
import requests
import json
from django.conf import settings
import logging
from django.http import JsonResponse
from master.globalparamters import get_auth_headers
API_URL = settings.API_URL

logger = logging.getLogger('erp_ui')


class LeadQuotationCreateView(View):
   
   def get(self,request,format=None):
      return render(request, 'crm/lead_quotation/lead_quotation_create.html')
   
   def post(self,request,*args):
      try:
         headers = get_auth_headers(request)

         response = requests.post(
               API_URL + '/crm/leadQuotation/create',
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


class LeadQuotationListView(View):
   
   def get(self,request,format=None):
      return render(request, 'crm/lead_quotation/lead_quotation_list.html')
   


class LeadQuotationListDataView(View):

   def get(self,request, *args, **kwargs):
      headers = get_auth_headers(request)

      api_url = API_URL + '/crm/leadQuotation/list'

      response = requests.get(api_url, headers=headers)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)


class LeadQuotationEMIScheduleView(View):

   def get(self, request, *args, **kwargs):
      try:
         headers = get_auth_headers(request)
         
         json_data = json.dumps({
            'loan_amount': request.GET.get('loanAmount'),
            'interest_rate': request.GET.get('interestRate'),
            'tenure': request.GET.get('tenure'),
         })

         api_url = API_URL + '/crm/leadQuotation/getEmiSchedule'
         response = requests.get(api_url + '?jsonData=' + json_data, headers=headers, timeout=30)

         if response.status_code == 200:
            return JsonResponse(response.json(), status=200)
         else:
            return JsonResponse(response.json(), status=response.status_code)

      except requests.exceptions.Timeout:
         return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)
      except requests.exceptions.RequestException as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=502)
      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)