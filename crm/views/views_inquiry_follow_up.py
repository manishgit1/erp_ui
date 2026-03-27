from django.views.generic import CreateView, View, ListView
from django.shortcuts import render
import requests
from django.conf import settings
import logging
from django.http import JsonResponse
from master.globalparamters import get_auth_headers
API_URL = settings.API_URL
import json
import ast

logger = logging.getLogger('erp_ui')


class InquiryFollowUpListView(View):
   
   def get(self,request,format=None):
      return render(request, 'crm/inquiry_follow_up/inquiry_follow_up_list.html')
   

class InquiryFollowUpListDataView(View):

   def get(self,request, *args, **kwargs):
      headers = get_auth_headers(request)
      api_url = API_URL + '/crm/inquiryFollowUp/list'

      response = requests.get(api_url, headers=headers)

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)