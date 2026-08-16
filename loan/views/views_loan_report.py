from django.views.generic import TemplateView, View
from django.http import JsonResponse
from master.globalparamters import api_request
import json

class LoanReportsView(TemplateView):
    template_name = 'loan/loan_reports/loan_report.html'

class LoanReportsDataView(View):
    def get(self, request, *args, **kwargs):
        jsonData = request.GET.get('jsonData', '{}')
        
        # Proxy request to erp_api
        response = api_request(
            request, 
            'GET', 
            '/loan/loanReport/list', 
            params={'jsonData': jsonData}
        )
        
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            try:
                return JsonResponse(response.json(), status=response.status_code)
            except ValueError:
                return JsonResponse(
                    {'resultCode': '1', 'resultDescription': 'Error from API'}, 
                    status=response.status_code
                )
