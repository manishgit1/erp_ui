from django.views.generic import View,ListView
import json
import requests
from django.conf import settings
from django.http import JsonResponse


API_URL = settings.API_URL

class GetBusinessDateView(View):

   def get(self,request, format=None):

      api_url = API_URL + '/tools/systemDate/getDate'
      response = requests.get(api_url, headers={})

      if response.status_code == 200:
         return JsonResponse(response.json(), status=200)
      else:
         return JsonResponse(response.json(), status=500)