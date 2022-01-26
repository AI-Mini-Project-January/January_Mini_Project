from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.home),
    path('kakaologinhome/', views.kakaologin),
]