from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    path('kakaoLogout/', views.kakaoLogout),
    path('kakaomessage_climate/', views.kakaoMessage_climate),
    path('kakaomessage_password/', views.kakaoMessage_password),
]