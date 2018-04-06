from django.urls import path

from shop.views import product_list, product_detail

app_name = 'shop'
urlpatterns = [
    path('<slug:category_slug>/', product_list, name='product_list_category'),
    path('<int:product_id>/<slug:slug>/', product_detail, name='product_detail'),
    path('', product_list, name='product_list'),
]
