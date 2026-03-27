import re
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware that redirects unauthenticated users to the login page.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Paths that do not require authentication
        self.exempt_urls = [
            r'^$',                        # Root (login)
            r'^user/login$',              # Login
            r'^user/register$',           # Register
            r'^user/register/create$',    # Register creation API
            r'^admin/',                   # Admin panel
        ]
        
        # Add any additional exempt URLs from settings
        if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
            self.exempt_urls += settings.LOGIN_EXEMPT_URLS

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        
        # 1. Allow static files and media
        if request.path.startswith(settings.STATIC_URL) or (settings.MEDIA_URL and request.path.startswith(settings.MEDIA_URL)):
            return self.get_response(request)

        # 2. Check if user is authenticated (access_token in session)
        is_authenticated = request.session.get('access_token') is not None
        
        # 3. Check if path is exempt
        is_exempt = any(re.match(url, path) for url in self.exempt_urls)

        if not is_authenticated and not is_exempt:
            # If it's an AJAX request or expects JSON, return 401 instead of redirect
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                from django.http import JsonResponse
                return JsonResponse({
                    'resultCode': '-401',
                    'resultDescription': 'Authentication required'
                }, status=401)
            
            return redirect('user-login')

        response = self.get_response(request)
        return response
