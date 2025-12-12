from django.views.generic import CreateView, View, ListView
from django.shortcuts import render
import requests
from django.conf import settings
import logging
from django.http import JsonResponse
API_URL = settings.API_URL

logger = logging.getLogger('django')


class LeadQuotationCreateView(View):
   
   def get(self,request,format=None):
      return render(request, 'crm/lead_quotation/lead_quotation_create.html')
   
   def post(self,request,*args):
      try:
         headers = {
               "Content-Type": request.META.get("CONTENT_TYPE", "application/json")
         }

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
      # data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      # data = request.GET.get('jsonData')
      headers = {
               #  'Authorization': request.session.get('authdata'),
               #  'Temp-Session-Id': request.session.get('temp_session_id')
      }

      api_url = API_URL + '/crm/leadQuotation/list'

      response = requests.get(api_url, headers=headers)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)