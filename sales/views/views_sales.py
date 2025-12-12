from django.views.generic import CreateView, View, ListView
from django.shortcuts import render


class SalesListView(CreateView):
   
   def get(self,request,format=None):
      print("sales template rendered")
      return render(request, 'sales/sales_list.html')