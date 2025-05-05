from django.urls import path
from .views import OrderCreateView, OrderListGetDataView, OrderListGetView

urlpatterns = [
     path('create', OrderCreateView.as_view(), name='orders-create'),
     path('ordersList', OrderListGetDataView.as_view(), name='orders-list-data'),
     path('myOrders', OrderListGetView.as_view(), name='orders-list'),
]