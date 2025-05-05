from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
import requests
from django.core.exceptions import ValidationError



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
            request.session['isAdmin'] = response['isAdmin']
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
        # headers = request.headers
        response = requests.post(request_url,data=request.data)
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