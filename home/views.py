from django.shortcuts import render, redirect
from django.views.generic import View, ListView


class DashboardView(View):
   
   def get(self,request, *args, **kwargs):
     username = request.GET.get('username')

   #   if request.session.get('isAdmin'):
   #      return render(request, 'home/home_admin.html')
     if request.session.get('temp_session_id'):
         return render(request, 'home/home.html', {'username': username})
     return render(request, 'home/error_404.html')



# def home_page(request):
#  return render(request, 'home/base.html')

class CartItemsView(ListView):
   def get(self,request, *args, **kwargs):
      
    if request.session.get('authdata'):
      return render(request, 'home/shopping_cart.html')
    else:
      return None