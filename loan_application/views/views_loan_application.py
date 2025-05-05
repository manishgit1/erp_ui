from django.views.generic import View
from django.shortcuts import render

class LoanApplicationCreateView(View):
   
   def get(self,request):
      return render(request,'loan_application/loan_application_create.html')
   
   