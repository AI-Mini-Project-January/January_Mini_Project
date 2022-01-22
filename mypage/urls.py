from django.urls import path
from . import views

urlpatterns = [
 path('member_info/', views.member_info),
]