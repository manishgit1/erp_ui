from django.shortcuts import render, redirect
import json
import requests
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.conf import settings
import logging

logger = logging.getLogger('erp_ui')


# Create your views here.

def validate_login_request(request, request_url):
    try: 
        json_error = []
        data = json.loads(request.body)
        username = data['username'] if 'username' in data else ''
        password = data['password'] if 'password' in data else ''
       
        if not username or not password:
            json_error.append("Username or password is missing")
        if json_error:
            error_message = {
                'resultCode': '-100',
                'resultDescription': json_error
            }
            return JsonResponse(error_message, status=400)
        response = requests.post(request_url, data=data)
        if response.status_code == 200:
            response = response.json()

            success_message = {
                'resultCode': '0',
                'resultDescription': 'Success',
            }


            request.session['username'] = response['username']
            # request.session['isAdmin'] = response['isAdmin']
            # request.session['aut?hdata'] = response['token']
            request.session['temp_session_id'] = response['temp_session_id']
            

            return JsonResponse(success_message, status=200)
   
    except Exception as e:
       raise ValidationError("Invalid credentials")
        


def validate_get_render_request(request, template_name, context=None):
    return render(request, template_name, context)



def validate_create_post_request(request, request_url):
    try:
        # data = json.loads(request.body)
        headers = get_auth_headers(request)
        response = requests.post(request_url,data=request.data, headers=headers)
        print(response)
        if response.status_code == 200:
            success_message = {
                'resultCode': '0',
                'resultDescription': 'Order Created Successfully'
            }
            return JsonResponse(success_message, status=200)
        
        else:
            error = {
                'resultCode': '-100',
                'resultDescription': 'Something Went Wrong'
            }
            return False
    
    except Exception as e:
        error = {
            'resultCode': '-104',
            'resultDescription': 'Internal Server Error'
        }
        return JsonResponse(error, status=500)
    

# def get_auth_headers(request):
#     """
#     Returns the common headers required for erp_api requests, 
#     including the Temp-Session-Id from the current session.
#     """
#     temp_session_id = request.session.get('temp_session_id')
#     headers = {
#         'Content-Type': 'application/json',
#     }
#     if temp_session_id:
#         headers['Temp-Session-Id'] = temp_session_id
    
#     return headers


def get_auth_headers(request):
    """
    Returns the common headers required for API requests,
    using JWT tokens stored in the current Django session.
    """
    access_token = request.session.get("access_token") 
    headers = {
        "Content-Type": "application/json",
    }

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    return headers


def validate_login_request_jwt(request, request_url):
    try: 
        data = json.loads(request.body)
        
        # If it's not an encrypted payload, validate username and password
        if 'payload' not in data:
            username = data.get('username', '')
            password = data.get('password', '')
           
            if not username or not password:
                return JsonResponse({
                    'resultCode': '-100',
                    'resultDescription': 'Username or password is missing'
                }, status=400)

        # Forward the data as JSON to the backend API
        response = requests.post(request_url, json=data)
        response_data = response.json()

        if response.status_code == 200:
            request.session['access_token'] = response_data.get('access_token')
            request.session['refresh_token'] = response_data.get('refresh_token')
            request.session.save()

        return JsonResponse(response_data, status=response.status_code)
   
    except Exception as e:
        return JsonResponse({
            'resultCode': '-500',
            'resultDescription': 'Internal Server Error',
            'error': str(e)
        }, status=500)



def api_request(request, method, endpoint, data=None, params=None, retries=1):
    """
    Global API request helper that:
    1. Adds access token to headers
    2. Refreshes token automatically if 401
    """
    access_token = request.session.get("access_token")
    refresh_token = request.session.get("refresh_token")

    headers = {
        "Content-Type": "application/json",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    url = f"{settings.API_URL}{endpoint}"

    response = requests.request(method, url, headers=headers, json=data, params=params)

    # If token expired, refresh once
    if response.status_code == 401 and retries > 0 and refresh_token:
        logger.debug(f"Access token expired. Attempting refresh for endpoint: {endpoint}")
        refresh_url = f"{settings.API_URL}/api/token/refresh/"
        try:
            refresh_resp = requests.post(refresh_url, json={"refresh": refresh_token})
            if refresh_resp.status_code == 200:
                refresh_data = refresh_resp.json()
                # Check for both 'access' and 'access_token' keys
                new_access = refresh_data.get("access") or refresh_data.get("access_token")
                
                if new_access:
                    logger.debug("Token refresh successful.")
                    request.session["access_token"] = new_access
                    request.session.save()
                    # Retry the original request
                    return api_request(request, method, endpoint, data, params, retries=retries-1)
                else:
                    logger.error(f"Refresh response successful but no access token found: {refresh_data}")
            else:
                logger.warning(f"Refresh failed. Status: {refresh_resp.status_code}, Body: {refresh_resp.text}")
        except Exception as e:
            logger.error(f"Exception during token refresh: {str(e)}")

        # If we reach here, refresh failed
        logger.info("Session expired or refresh failed. Clearing tokens and flushing session.")
        request.session.flush()
        # Optionally, you could just pop the tokens if you want to keep other session data:
        # request.session.pop("access_token", None)
        # request.session.pop("refresh_token", None)
        
        raise Exception("Session expired, please login again")

    return response