from django.urls import path
from .views import  ProductListsDataView, ProductCreateView, ProductDetailView, ProductDataByIdView, ProductsListView

urlpatterns = [
     path('createProduct',ProductCreateView.as_view(), name='create-products'),
     path('products', ProductsListView.as_view(), name='products'),
     path('productsList', ProductListsDataView.as_view(), name='products-lists'),
     path('productDetail', ProductDetailView.as_view(), name='product-detail'),
     path('<int:pk>/findById', ProductDataByIdView.as_view(), name='product-data'),
     
]