from django.shortcuts import render

# Create your views here.


def dashboard(request):
  menu_items = [
        {"name": "Products", "url": "/products/", "icon": "fas fa-box", "description": "Manage products and stock"},
        {"name": "Customers", "url": "/master/customerOnboarding/list", "icon": "fas fa-users", "description": "Customer records"},
        {"name": "Loan Application", "url": "/crm/leadQuotation/create", "icon": "fas fa-file-invoice-dollar", "description": ""},
        {"name": "Sales Orders", "url": "/sales-orders/", "icon": "fas fa-shopping-cart", "description": "Track confirmed orders"},
        {"name": "Invoices", "url": "/invoices/", "icon": "fas fa-receipt", "description": "Manage billing"},
        {"name": "Payments", "url": "/payments/", "icon": "fas fa-credit-card", "description": "Track payments"},
      ]  
  return render(request, 'base.html', {'menuItems': menu_items})