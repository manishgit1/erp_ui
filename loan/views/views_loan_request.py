from django.views.generic import View
from django.shortcuts import render
from django.conf import settings
from master.globalparamters import api_request,get_auth_headers
import requests
import json
from django.http import JsonResponse
import logging

API_URL = settings.API_URL

logger = logging.getLogger('erp_ui')

class LoanRequestCreateView(View):
    def get(self, request, *args, **kwargs):
        data = request.GET.get('jsonData')
        context = {
            'data': data
        }
        return render(request, 'loan/loan_request/loan_request_create.html', context)

    def post(self,request,*args):
      try:
         headers = get_auth_headers(request)

         response = requests.post(
               API_URL + '/loan/loanRequest/create',
               data=request.body,
               headers=headers,
               timeout=30
         )

         return JsonResponse(
                response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text, status=response.status_code)

      except requests.exceptions.Timeout:
         logger.error("API request timed out.", exc_info=True)
         return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)

      except requests.exceptions.RequestException as e:
         logger.error("API request failed.", exc_info=True)
         return JsonResponse({"status": "error", "message": str(e)}, status=502)

      except Exception as e:
         logger.error(str(e), exc_info=True)
         return JsonResponse({"status": "error", "message": str(e)}, status=500)

class LoanRequestListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'loan/loan_request/loan_request_list.html')

class LoanRequestListJsonView(View):
    def get(self, request, *args, **kwargs):
      try:
         headers = get_auth_headers(request)

         response = requests.get(
               API_URL + '/loan/loanRequest/list',
               headers=headers,
               timeout=30
         )

         return JsonResponse({
               "status": "success" if response.ok else "error",
               "status_code": response.status_code,
               "datas": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
         }, status=response.status_code)

      except requests.exceptions.Timeout:
         logger.error("API request timed out.", exc_info=True)
         return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)

      except requests.exceptions.RequestException as e:
         logger.error("API request failed.", exc_info=True)
         return JsonResponse({"status": "error", "message": str(e)}, status=502)

      except Exception as e:
         logger.error(str(e), exc_info=True)
         return JsonResponse({"status": "error", "message": str(e)}, status=500)



class LoanRequestDataByIdView(View):
   def get(self,request,pk,format=None):
      api_url = API_URL + '/loan/loanRequest/' + str(pk) + '/findById'
      headers = get_auth_headers(request)
      response = requests.get(api_url, headers=headers)
      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)



class PendingLoansDataView(View):
    def get(self, request, *args, **kwargs):
      try:
         headers = get_auth_headers(request)
         response = requests.get(API_URL + '/loan/loanRequest/pending/list', headers=headers, timeout=30)
         return JsonResponse(response.json() if response.ok else [], status=response.status_code)
      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)

class RevertedLoansDataView(View):
    def get(self, request, *args, **kwargs):
      try:
         headers = get_auth_headers(request)
         response = requests.get(API_URL + '/loan/loanRequest/reverted/list', headers=headers, timeout=30)
         return JsonResponse(response.json() if response.ok else [], status=response.status_code)
      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)

class RejectedLoansDataView(View):
    def get(self, request, *args, **kwargs):
      try:
         headers = get_auth_headers(request)
         response = requests.get(API_URL + '/loan/loanRequest/rejected/list', headers=headers, timeout=30)
         return JsonResponse(response.json() if response.ok else [], status=response.status_code)
      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)

class ApprovedLoansDataView(View):
    def get(self, request, *args, **kwargs):
      try:
         headers = get_auth_headers(request)
         response = requests.get(API_URL + '/loan/loanRequest/approved/list', headers=headers, timeout=30)
         return JsonResponse(response.json() if response.ok else [], status=response.status_code)
      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)

class DisbursedLoansDataView(View):
    def get(self, request, *args, **kwargs):
      try:
         headers = get_auth_headers(request)
         response = requests.get(API_URL + '/loan/loanRequest/disbursed/list', headers=headers, timeout=30)
         return JsonResponse({"status": "success" if response.ok else "error", "datas": response.json() if response.ok else []}, status=response.status_code)
      except Exception as e:
         return JsonResponse({"status": "error", "message": str(e)}, status=500)

class LoanRequestApproveView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            response = api_request(request, 'POST', '/loan/loanRequest/approveRejectRevert', data=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)

class LoanRequestRejectView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            response = api_request(request, 'POST', '/loan/loanRequest/reject', data=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)

class LoanRequestRevertView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            response = api_request(request, 'POST', '/loan/loanRequest/revert', data=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)

class LoanRequestTimelineDataView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            headers = get_auth_headers(request)
            response = requests.get(f"{API_URL}/loan/loanRequest/{pk}/timeline", headers=headers, timeout=30)
            return JsonResponse(response.json() if response.ok else [], status=response.status_code, safe=False)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

class LoanRequestDisburseView(View):
    def get(self, request, *args, **kwargs):
        data = request.GET.get('jsonData')
        context = {
            'data': data
        }
        return render(request, 'loan/loan_request/loan_disbursement.html', context)
