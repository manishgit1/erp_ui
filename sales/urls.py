from django.urls import path
from sales import views
urlpatterns = [
 path('list', views.SalesListView.as_view(), name='sales-list'),
]