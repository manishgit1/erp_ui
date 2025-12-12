from django.urls import path
from tools import views

urlpatterns = [
   path('loanType/create',views.LoanTypeCreateView.as_view(), name='loan-type-create'),
   path('loanType/list',views.LoanTypeListView.as_view(), name='loan-type-list'),
   path('loanType/lists',views.LoanTypeListDataView.as_view(), name='loan-type-lists'),
   path('leadSource/create',views.LeadSourceCreateView.as_view(), name='lead-source-create'),
   path('leadSource/list', views.LeadSourceListView.as_view(), name='lead-source-list'),
   path('leadSource/lists', views.LeadSourceListDataView.as_view(), name='lead-source-lists'),
   path('tools/list', views.ToolsListView.as_view(), name='tools-template-view'),

   path('clientType/list', views.ClientTypeListView.as_view(), name='client-type-list'),
   path('clientType/lists', views.ClientTypeListDataView.as_view(), name='client-type-lists'),
   path('clientType/create', views.ClientTypeCreateView.as_view(), name='client-type-create'),

   path('systemDate/getDate',views.GetBusinessDateView.as_view(),name='get-business-date'),
]