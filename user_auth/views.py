from master.globalparamters import validate_login_request_jwt, api_request
from django.shortcuts import render, redirect
from django.views.generic import View
from master.globalparamters import validate_login_request, validate_get_render_request
import json
from django.conf import settings
import logging
import requests
from django.http import JsonResponse


logger = logging.getLogger('erp_ui')

API_BASE_URL = settings.API_URL

def login_user(request):
  return render(request, 'user_auth/login.html')

def register_user(request):
  return render(request, 'user_auth/register.html')



class RegisterView(View):
    
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'user_auth/register.html')
    
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
          request_url =  API_BASE_URL + 'master/user/register'
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
       return validate_get_render_request(request, 'user_auth/login.html')
   
   def post(self,request,*args, **kwargs):
      try:
        response = validate_login_request_jwt(request, API_BASE_URL + '/auth/user/login')
        return response
            
      except Exception as e:
        logger.error(str(e), exc_info=True)
        raise ValueError('Login fields missing!')
      
      


class Logout(View):

    def get(self, request, *args, **kwargs):

        request_url = API_BASE_URL + '/auth/user/logout'

        access_token = request.session.get("access_token")
        refresh_token = request.session.get("refresh_token")

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        data = {
            "refresh": refresh_token
        }

        response = requests.post(
            request_url,
            json=data,
            headers=headers
        )

        request.session.flush()

        if response.status_code == 200:
            return JsonResponse({
                "resultCode": "0",
                "resultDescription": "Successfully logged out"
            }, status=200)

        return JsonResponse({
            "resultCode": "-1",
            "resultDescription": "Logout failed"
        }, status=400)


# ─── Settings Menu ───────────────────────────────────────────────────────────

class SettingsMenuView(View):
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'user_auth/settings/settings_menu.html')


# ─── User Setup Views ─────────────────────────────────────────────────────────

class UserSetupListView(View):
    """Renders the user setup list page."""
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'user_auth/user_setup/user_setup_list.html')


class UserSetupListDataView(View):
    """Proxies list of users from the backend API."""
    def get(self, request, *args, **kwargs):
        try:
            response = api_request(request, 'GET', '/auth/user/list')
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)


class UserSetupCreateView(View):
    """Renders the create-user form page."""
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'user_auth/user_setup/user_setup_create.html')
    

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            response = api_request(request, 'POST', '/auth/user/create', data=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)


class UserSetupEditView(View):
    """Renders the edit-user form page."""
    def get(self, request, pk, *args, **kwargs):
        context = {'user_id': pk}
        return validate_get_render_request(request, 'user_auth/user_setup/user_setup_edit.html', context)

    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            response = api_request(request, 'POST', '/auth/user/edit', data=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)

class UserSetupFindByIdAPIView(View):
    """Fetches a single user by ID from backend API."""
    def get(self, request, user_id, *args, **kwargs):
        try:
            response = api_request(request, 'GET', f'/auth/user/{user_id}/find')
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)




# ─── Role Setup Views ─────────────────────────────────────────────────────────

class RoleSetupListView(View):
    """Renders the role setup list page."""
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'user_auth/role_setup/role_setup_list.html')


class RoleSetupListDataView(View):
    """Proxies list of roles from the backend API."""
    def get(self, request, *args, **kwargs):
        try:
            response = api_request(request, 'GET', '/auth/role/list')
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)


class RoleSetupCreateView(View):
    """Renders the create-role form page."""
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'user_auth/role_setup/role_setup_create.html')

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            response = api_request(request, 'POST', '/auth/role/create', data=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)


class RoleSetupEditView(View):
    """Renders the edit-role form page."""
    def get(self, request, pk, *args, **kwargs):
        context = {'role_id': pk}
        return validate_get_render_request(request, 'user_auth/role_setup/role_setup_edit.html', context)
    

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            response = api_request(request, 'POST', '/auth/role/edit', data=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)

class RoleSetupFindByIdAPIView(View):
    """Fetches a single role by ID from backend API."""
    def get(self, request, role_id, *args, **kwargs):
        try:
            response = api_request(request, 'GET', f'/auth/role/{role_id}/findById')
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)

# ─── Workflow Setup Views ───────────────────────────────────────────────────

class WorkflowSetupListView(View):
    """Renders the workflow setup list page."""
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'user_auth/workflow_setup/workflow_setup_list.html')


class WorkflowSetupListDataView(View):
    """Proxies list of workflows from the backend API."""
    def get(self, request, *args, **kwargs):
        try:
            response = api_request(request, 'GET', '/loan/workflow/list')
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)


class WorkflowSetupCreateView(View):
    """Handles workflow template rendering and creation proxy."""
    def get(self, request, *args, **kwargs):
        return validate_get_render_request(request, 'user_auth/workflow_setup/workflow_setup_create.html')

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            # The URL to backend API for workflow creation
            response = api_request(request, 'POST', '/loan/workflow/create', data=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return JsonResponse({'resultCode': '-500', 'resultDescription': str(e)}, status=500)
