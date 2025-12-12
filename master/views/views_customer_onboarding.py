from django.views.generic import CreateView, View
from django.shortcuts import render

class CustomerOnBoardingView(CreateView):
   def get(self,request, format=None):
      return render(request, 'master/customer_onboarding/customer_onboarding.html')
