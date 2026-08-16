from django.urls import path
from master import views

urlpatterns = [
     path('',views.dashboard, name='dashboard' ),
     path('contact/list', views.GlobalContactListView.as_view(), name='contact-master-list'),
     path('contact/create', views.GlobalContactCreateView.as_view(), name='contact-master-create'),
     path('contact/<pk>/edit', views.GlobalContactEditView.as_view(), name='contact-master-edit'),
     path('contact/<pk>/findById', views.GlobalContactDataByIdView.as_view(), name='contact-master-data-by-id'),
     path('contact/lists', views.GlobalContactListDataView.as_view(), name='contact-master-lists'),

     path('customerOnboarding/list', views.CustomerOnBoardingView.as_view(), name='customer-onboarding-page'),

     path('clientMaster/list', views.ClientMasterListView.as_view(), name='client-master-list'),
     path('clientMaster/lists',views.ClientMasterListDataView.as_view(), name='client-master-lists'),
     path('clientMaster/create', views.ClientMasterCreateView.as_view(), name='client-master-create'),
     path('clientMaster/<str:pk>/update', views.ClientMasterUpdateView.as_view(), name='client-master-update'),
     path('clientMaster/<str:pk>/findById', views.ClientMasterDataByIdView.as_view(), name='client-master-data-by-id'),
     path('clientMaster/<str:pk>/edit', views.ClientMasterEditView.as_view(), name='client-master-edit'),
     path('clientMaster/checkIfClientExists/', views.ClientMasterCheckIfClientExistsView.as_view(), name='client-master-check-if-client-exists'),
     path('clientMaster/getLeadData/', views.ClientMasterGetLeadDataView.as_view(), name='client-master-get-lead-data'),
     path('generalSettings/lists',views.GeneralSettingsListDataView.as_view(), name='general-settings-lists'),
     path('contact/checkIfContactExists/', views.CheckIfContactExistsView.as_view(), name='check-if-contact-exists'),

     path('getAddressInfo/', views.GetAddressByMunicipalityView.as_view(), name='get-address-by-municipality'),
     path('dashboard/metrics/', views.DashboardMetricsView.as_view(), name='dashboard-metrics'),


]