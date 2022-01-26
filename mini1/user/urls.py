from django.urls import path
from . import views
from .views import Join, Login, Logout, UploadProfile

# urls를 join이라고 해도 앱이름이 user이기 때문에 ~/user/join 으로 들어감
urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('logout', Logout.as_view()),
    path('profile/upload', UploadProfile.as_view()),


    #카카오 메시지 보내기 위한 로그인
    path('user/kakaologinhome/', views.kakaologinHome),
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