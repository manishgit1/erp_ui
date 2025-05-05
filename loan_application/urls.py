from django.urls import path
from loan_application import views

urlpatterns = [
 path('lead/create', views.LoanApplicationCreateView.as_view(), name='loan-application-create'),
]