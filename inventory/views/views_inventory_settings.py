from django.views.generic import CreateView, View, ListView
from django.shortcuts import render


class InventorySettingsListView(View):
   
   def get(self,request,format=None):
      
     menu_items = [
        {"name": "Products", "url": "/products/", "icon": "fas fa-box", "description": "Manage products and stock"},
        {"name": "Customers", "url": "/customers/", "icon": "fas fa-users", "description": "Customer records"},
        {"name": "Quotations", "url": "/quotations/", "icon": "fas fa-file-invoice-dollar", "description": "Create and send quotes"},
        {"name": "Sales Orders", "url": "/sales-orders/", "icon": "fas fa-shopping-cart", "description": "Track confirmed orders"},
        {"name": "Invoices", "url": "/invoices/", "icon": "fas fa-receipt", "description": "Manage billing"},
        {"name": "Payments", "url": "/payments/", "icon": "fas fa-credit-card", "description": "Track payments"},
      ]  
     
     return render(request, 'inventory/inventory.html', {'menuItems': menu_items})
   

