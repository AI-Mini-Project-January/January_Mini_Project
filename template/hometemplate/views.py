from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
import requests
import json

# Create your views here.

def home(request):
    return render(request, 'hometemplate/index.html')

# def kakaologinhome(request):
#     return render(request, 'hometemplate/kakaologinhome.html')

def kakaologin(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'hometemplate/kakaologinhome.html', _context)

def kakaoLoginLogic(request):
    _restApiKey = '5d03e24af9d6c95a6f526e3308d8879d' # 입력필요
    _redirectUrl = 'http://127.0.0.1:8000/home/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = '5d03e24af9d6c95a6f526e3308d8879d' # 입력필요
    _redirect_uri = 'http://127.0.0.1:8000/home/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    return render(request, 'hometemplate/kakaologinSuccess.html')

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
        return render(request, 'hometemplate/kakaologinhome.html')
    else:
        return render(request, 'hometemplate/kakaologoutError.html')

#날씨 요약 정보
def kakaoMessage_climate(request):
    temperature = 24
    rain = 30
    cloth = ""

    if temperature <= 4:
        cloth = "패딩, 목도리, 장갑 매우 추워요"
    elif temperature >= 5 and temperature <= 8:
        cloth = "울코트, 기모"
    elif temperature >= 9 and temperature <= 11:
        cloth = "트렌치 코트, 점퍼"
    elif temperature >= 12 and temperature <= 16:
        cloth = "가디건, 청자켓, 청바지"
    elif temperature >= 17 and temperature <= 19:
        cloth = "후드티, 맨투맨"
    elif temperature >= 20 and temperature <= 22:
        cloth = "블라우스, 슬랙스"
    elif temperature >= 23 and temperature <= 27:
        cloth = "반팔, 반바지, 얇은 셔츠"
    else:
        cloth = "시원하게 입기"



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
            "text": "오늘의 날씨 요약 정보는 \n" + "기온 : " + (str)(temperature) + "'C\n강수확률 : " + (str)(rain) + "% 이므로\n오늘의 옷차림은 " + cloth + "를 추천드립니다.",
            "link":{
                "web_url":"http://127.0.0.1:8000/home/index"
            }
        })
    }

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
    return render(request, 'hometemplate/kakaoMessageSent.html')