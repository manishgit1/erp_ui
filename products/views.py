from django.shortcuts import render
from django.views.generic import ListView, CreateView, View
from django.conf import settings
import requests
from django.http import JsonResponse
import json

# Create your views here.


API_BASE_URL = settings.API_BASE_URL


class ProductsListView(ListView):
    def get(self, request, *args, **kwargs):
        return render(request, 'products/products_view_admin.html')



class ProductListsDataView(ListView):
     
     def get(self,request, *args, **kwargs):
        request_url = API_BASE_URL + "/products/getProducts" 
        response = requests.get(request_url)
        data = response.json()
        return JsonResponse(data, status=200, safe=False)



class ProductCreateView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'products/products_create.html')

    def post(self, request, *args, **kwargs):
        try:
            # Extract form data
            name = request.POST.get('name')
            description = request.POST.get('description')
            tags = request.POST.get('tags')
            price = request.POST.get('price')

            # Prepare data for API
            product_data = {
                'name': name,
                'description': description,
                'tags': tags,
                'price': price
            }

            

            # Handle file uploads
            files = [('images', img) for img in request.FILES.getlist('images')]

            # Send request to external API
            request_url = f"{API_BASE_URL}products/create"
            response = requests.post(request_url, data=product_data, files=files)

            # Handle API response
            json_data = response.json()
            return JsonResponse(json_data, status=response.status_code)

        except Exception as e:
            return JsonResponse({'resultCode': '1', 'resultDescription': str(e)}, status=500)

   
class ProductDetailView(View):
    
    def get(self,request, *args, **kwargs):
        id = request.GET.get('jsonData')
        api_base_url = settings.API_BASE_URL

        return render(request, 'products/product_detail.html', context={'id': id, 'api_base_url': api_base_url})


class ProductDataByIdView(View):
    def get(self,request, pk , *args, **kwargs):
        request_url = API_BASE_URL + f"products/{pk}/findById"
        response = requests.get(request_url, data=None)

        return JsonResponse(response.json(), status=200)
    
