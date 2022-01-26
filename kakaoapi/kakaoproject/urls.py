from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    path('kakaoLogout/', views.kakaoLogout),

    #날씨 요약 정보
    path('kakaomessage_climate/', views.kakaoMessage_climate),
    #패스워드 찾기
    path('loginSuccess/', views.password_throw),
    # path('passwordckeck/', views.password_check),
    path('password/', views.kakaoMessage_password),
]
