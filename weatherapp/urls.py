from django.urls import path
from . import views

app_name = 'weatherapp'

urlpatterns = [
    path('get_weather/', views.get_weather),
    path('get_clothes/', views.get_clothes),

]