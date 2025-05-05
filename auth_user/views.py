from django.shortcuts import render
from django.views.generic import View
from globalparameters.views import validate_login_request, validate_get_render_request
import json
from django.conf import settings
import logging
import requests
from django.http import JsonResponse


logger = logging.getLogger('django')

API_BASE_URL = settings.API_BASE_URL

def login_user(request):
  return render(request, 'auth_user/login.html')

def register_user(request):
  return render(request, 'auth_user/register.html')



class RegisterView(View):
    
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'auth_user/register.html')
    
    def post(self,request,*args, **kwargs):
        try:
          data = json.loads(request.body)
          first_name = data['firstName'] if 'firstName' in data else ''
          last_name = data['lastName'] if 'lastName' in data else ''
          username = data['username'] if 'username' in data else ''
          password = data['password'] if 'password' in data else ''
          confirm_password = data['confirmPassword'] if 'confirmPassword' in data else ''

          
          if not first_name or not last_name or not username or not password or not confirm_password:
              return JsonResponse({'resultCode': '-100', 'resultDescription': 'All fields are required'}, status=400)
          if confirm_password != password:
              return JsonResponse({'resultCode': '-100', 'resultDescription': 'Passwords do not match'}, status=400)
          request_url = API_BASE_URL + 'master/user/register'
          print(request_url)
          headers = {
              'Content-Type': 'application/json'
          }
          response = requests.post(request_url, data = json.dumps(data), headers=headers)
          if response.status_code == 200:
              return JsonResponse(response.json(), status=200)
          return JsonResponse({'resultCode': '-100', 'resultDescription': 'Error registering user'}, status=400)
              
        except Exception as e:
          logger.error(str(e), exc_info=True)
          raise ValueError('Register fields missing!')

class LoginView(View):
   
   def get(self, request, *args, **kwargs):
     
       return validate_get_render_request(request, 'auth_user/login.html')
   
   def post(self,request,*args, **kwargs):
      try:
        response = validate_login_request(request, API_BASE_URL + '/master/user/login')
        return response
            
      except Exception as e:
        logger.error(str(e), exc_info=True)
        raise ValueError('Login fields missing!')


class Logout(View):

  def get(self, request, *args, **kwargs):
      request_url = API_BASE_URL + 'master/user/logout'
      headers = {
                'Authorization': request.session.get('authdata'),
                'Temp-Session-Id': request.session.get('temp_session_id')
            }
      data = ""
      response = requests.get(request_url, data = json.dumps(data), headers=headers)

      if response.status_code == 200:

          if request.session.get('authdata'):
                    request.session.flush()
                    response = {
                        'resultCode': '0',
                        'resultDescription': 'Successfully logged out'
                    }
                    return JsonResponse(response, status=200)
                
                # If user is not logged in
          return JsonResponse({'resultCode': '-100', 'resultDescription': 'User not logged in'}, status=400)