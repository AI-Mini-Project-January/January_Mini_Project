from django.shortcuts import render, redirect
import requests
import json
from django.template import loader
from django.http import HttpResponse, JsonResponse

# Create your views here.

def index(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'kakaoproject/index.html', _context)

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

def kakaoMessage(request):
    url_message = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    _token = request.session['access_token']

    _header = {
      'Authorization': f'bearer {_token}'
    }

    data={
        "template_object": json.dumps({
            "object_type":"text",
            "text":"홋Wealth 첫 테스트 메시지 _ 오늘의 날씨입니다.",
            "link":{
                "web_url":"www.naver.com"
            }
        })
    }

    _res = requests.post(url_message, headers=_header, data=data)
    _result = _res.json()

    return render(request, 'kakaoproject/message.html')