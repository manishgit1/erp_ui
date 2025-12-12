from django.views.generic import CreateView, View, ListView
from django.shortcuts import render
import requests
from django.conf import settings
import logging
from django.http import JsonResponse
API_URL = settings.API_URL
import json
import ast

logger = logging.getLogger('django')


class InquiryFollowUpListView(View):
   
   def get(self,request,format=None):
      return render(request, 'crm/inquiry_follow_up/inquiry_follow_up_list.html')
   

class InquiryFollowUpListDataView(View):

   def get(self,request, *args, **kwargs):
      # data = json.loads(json.dumps(ast.literal_eval(request.GET.get('jsonData'))))
      # headers = {
      #           'Authorization': request.session.get('authdata'),
      #           'Temp-Session-Id': request.session.get('temp_session_id')
      # }
      api_url = API_URL + '/crm/inquiryFollowUp/list'

      response = requests.get(api_url, headers={})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)