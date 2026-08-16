from django.shortcuts import render
from django.views.generic import View

# Create your views here.


def dashboard(request):
  menu_items = [
        # {"name": "Products", "url": "/products/", "icon": "fas fa-box", "description": "Manage products and stock"},
        {"name": "Customers", "url": "/master/customerOnboarding/list", "icon": "fas fa-users", "description": "Customer records"},
        {"name": "Lead Registration", "url": "/crm/leadQuotation/create", "icon": "fas fa-file-invoice-dollar", "description": ""},
        # {"name": "Sales Orders", "url": "/sales-orders/", "icon": "fas fa-shopping-cart", "description": "Track confirmed orders"},
        # {"name": "Invoices", "url": "/invoices/", "icon": "fas fa-receipt", "description": "Manage billing"},
        # {"name": "Payments", "url": "/payments/", "icon": "fas fa-credit-card", "description": "Track payments"},
      ]  
  return render(request, 'base.html', {'menuItems': menu_items})


class DashboardMetricsView(View):
    def get(self, request, *args, **kwargs):
        try:
            from master.globalparamters import get_auth_headers
            import requests
            from django.conf import settings
            from django.http import JsonResponse

            headers = get_auth_headers(request)
            api_url = settings.API_URL + '/master/dashboard/metrics/'

            response = requests.get(api_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return JsonResponse(response.json(), status=200)
            else:
                return JsonResponse(response.json() if "application/json" in response.headers.get("Content-Type", "") else {"message": response.text}, status=response.status_code)

        except requests.exceptions.Timeout:
            return JsonResponse({"status": "error", "message": "API request timed out."}, status=504)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)