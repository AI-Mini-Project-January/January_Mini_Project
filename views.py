from django.shortcuts import render, redirect
import requests
import json
from django.template import loader
from django.http import HttpResponse, JsonResponse

import kakaoproject.models as models
from .models import ClimateMessage, User

# Create your views here.

def home(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'kakaoproject/home.html', _context)

def kakaoLoginLogic(request):
    _restApiKey = '5d03e24af9d6c95a6f526e3308d8879d' # 입력필요
    _redirectUrl = 'http://127.0.0.1:8000/kakao/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = '5d03e24af9d6c95a6f526e3308d8879d' # 입력필요
    _redirect_uri = 'http://127.0.0.1:8000/kakao/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    return render(request, 'kakaoproject/loginSuccess.html')

def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    # _url = 'https://kapi.kakao.com/v1/user/unlink'
    # _header = {
    #   'Authorization': f'bearer {_token}',
    # }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'kakaoproject/loginoutSuccess.html')
    else:
        return render(request, 'kakaoproject/logoutError.html')

def kakaoMessage_climate(request):
    me = (str)(request.GET.get('user_id'))

    # climate = (str)(ClimateMessage.objects.filter(user_id=1).values("temperature"))

    climate = (str)(list(ClimateMessage.objects.filter(user__user_identi=me).values("temperature", "rain", "cloth")))
    # climate = (str)(ClimateMessage.objects.filter(user_id__user_identi = user))


    # climate = [temp, "https://icon-icons.com/ko/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%98%B7/80572", "http://127.0.0.1:8000/kakao/home"]
    # climate ={
    #     "title" : temp,
    #     "image_url" :"http://127.0.0.1:8000/kakao/home",
    #     "link" : "http://127.0.0.1:8000/kakao/home"
    # }

    # climate_list = {
    #     "temperature" : ClimateMessage.objects.filter(user_id=1).values("temperature"),
    #     "rain" : ClimateMessage.objects.filter(user_id=1).values("rain"),
    #     "cloth" : ClimateMessage.objects.filter(user_id=1).values("cloth"),
    # }

    url_message = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    _token = request.session['access_token']

    _header = {
      'Authorization': f'bearer {_token}'
    }
    
    # _nickname = "희동이누나"    #String
    # _today = "오늘의 날씨입니다."   #String

    data={
        "template_object": json.dumps({
            "object_type": "text",
            "text": "오늘의 날씨 요약 정보는 \n" + climate + " 입니다.",
            "link":{
                "web_url":"http://127.0.0.1:8000/kakao/index"
            }
        })
    }
    print(climate)

    # data = {
    #     "template_object" : json.dumps({
    #         "object_type": "list",
    #         "header_title": "오늘의 날씨입니다.",
    #         "header_link" : "http://127.0.0.1:8000/kakao/home",
    #         "contents" : climate
    #     })
    # }

    # print(climate_list)

    _res = requests.post(url_message, headers=_header, data=data)
    _result = _res.json()
    return render(request, 'kakaoproject/message.html')

def kakaoMessage_password(request):
    user = request.GET.get('user_id')

    ID = (str)(list(User.objects.filter(user_identi = user).values("user_identi")))
    password = (str)(list(User.objects.filter(user_identi = user).values("password")))

    url_message = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    _token = request.session['access_token']

    _header = {
      'Authorization': f'bearer {_token}'
    }
    
    _nickname = "희동이누나"    #String
    _password = "까먹으신 패스워드 입니다." #String

    data={
        "template_object": json.dumps({
            "object_type": "text",
            "text": ID + "님 패스워드는 " + password + "입니다.",
            "link":{
                "web_url":"http://127.0.0.1:8000/kakao/index"
            }
        })
    }

    _res = requests.post(url_message, headers=_header, data=data)
    _result = _res.json()
    return render(request, 'kakaoproject/message.html')