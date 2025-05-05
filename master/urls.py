from django.urls import path
from .views import ContactMasterCreateView, GeneralSettingsView,  GeneralSettingsCreateView, GeneralSettingsListDataView
urlpatterns = [
    path('contactMaster/get',ContactMasterCreateView.as_view(), name='contact-master-get' ),
    path('generalSettings/create', GeneralSettingsView.as_view(), name='general-settings-create'),
    path('generalSettings/list',GeneralSettingsListDataView.as_view(), name='general-settings-lists'),
    # path('generalSettings/province/create', GeneralSettingsCreateView.as_view(), name='general-settings-create'),
]