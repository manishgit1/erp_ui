from django.urls import path
from inventory import views

urlpatterns = [
 path('inventorySettings/list', views.InventorySettingsListView.as_view(), name='inventory-settings-list'),
 
]