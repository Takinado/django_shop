from django.urls import path

from .views import cupon_aplly

app_name = 'cupon'
urlpatterns = [
    path('apply/', cupon_aplly, name='aplly'),
]
