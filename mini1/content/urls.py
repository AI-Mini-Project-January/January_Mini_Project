from django.urls import path
from .views import UploadFeed, Profile # content.views에 있는 uploadFeed를 실행한다
from . import views

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('profile', Profile.as_view()),
    path('update', views.update),
] 
