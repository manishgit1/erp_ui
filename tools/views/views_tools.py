
from django.shortcuts import render
from django.views.generic import CreateView


class ToolsListView(CreateView):
   
   def get(self,request,format=None):
      return render(request, 'tools/tools.html')
   


