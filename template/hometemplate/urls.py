from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.home),
    path('kakaologinhome/', views.kakaologin),
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    path('kakaoLogout/', views.kakaoLogout),
    path('kakaomessage_climate/', views.kakaoMessage_climate),
]