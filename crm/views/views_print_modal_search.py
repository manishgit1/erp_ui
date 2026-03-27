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



class PrintModalSearchListDataView(View):

   def get(self,request, *args, **kwargs):
      headers = get_auth_headers(request)
      data = request.GET.get('jsonData')
      api_url = API_URL + '/crm/printModalSearch/search'

      response = requests.get(api_url, headers=headers,params={"jsonData": data})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)