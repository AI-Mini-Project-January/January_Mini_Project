from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from datetime import date, datetime, timedelta
import urllib
import urllib.request
import math

# google api geolocate를 활용하여 ip 주소를 기반으로 현재 위치의 위도, 경도 정보 추출
def get_location(request):
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBf9kIq9ciMUvzAr5neaJRMrlbx7rMZJx0'
    data = {'considerIp': True, } # 현 IP로 데이터 추출
    result = requests.post(url, data) # 해당 API에 요청을 보내며 데이터를 추출
    print(result.text)
    result2 = json.loads(result.text)

    lat = result2["location"]["lat"] # 현재 위치의 위도 추출
    lng = result2["location"]["lng"] # 현재 위치의 경도 추출

    return lat, lng


#get_location함수를 통해 위도와 경도 값을 넣고 x좌표, y좌표 얻어내기
def grid(lat, lng):
    v1 = lat
    v2 = lng

    Re = 6371.00877     ##  지도반경
    grid = 5.0          ##  격자간격 (km)
    slat1 = 30.0        ##  표준위도 1
    slat2 = 60.0        ##  표준위도 2
    olon = 126.0        ##  기준점 경도
    olat = 38.0         ##  기준점 위도
    XO = 43             ##  기준점 X좌표
    YO = 136            ##  기준점 Y좌표
    DEGRAD = math.pi / 180.0

    re = Re / grid
    slat1 = slat1 * DEGRAD  #표준위도1
    slat2 = slat2 * DEGRAD  #표준위도2
    olon = olon * DEGRAD    #기준점 경도
    olat = olat * DEGRAD    #기준점 위도

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)  
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)  
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)   
    ro = re * sf / math.pow(ro, sn)
    ra = math.tan(math.pi * 0.25 + (v1) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)

    theta = v2 * DEGRAD - olon

    if theta > math.pi :
        theta -= 2.0 * math.pi
    if theta < -math.pi :
        theta += 2.0 * math.pi
    theta *= sn

    x = math.floor(ra * math.sin(theta) + XO + 0.5)
    y = math.floor(ro - ra * math.cos(theta) + YO + 0.5)

    # x좌표, y좌표 리턴
    return x, y


def get_weather(request):

    #위도, 경도 함수 호출
    lat, lng = get_location(request)
    print(lat, lng)

    # x좌표, y좌표 함수 호출
    x, y = grid(lat, lng)
    print(x,y)

    # 기상청 단기예보 api
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

    today = datetime.today()

    base_date = today.strftime("%Y%m%d")
    today_date = today.strftime("%Y%m%d")
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_date = tomorrow.strftime("%Y%m%d")
    yesterday = date.today() - timedelta(days=1)
    yesterday_date = yesterday.strftime("%Y%m%d")

    time = today.strftime('%H%M')

    
    # 날씨 정보 발표 날짜와 시각(base_date, base_time) 
    # 하드코딩 대신 자동으로 시간 받아서 설정해주기

    hour = today.hour
    minute = today.minute
    
    if hour < 2 or (hour == 2 and minute <= 10):
        base_date = yesterday_date
        base_time = "2300"
    elif hour < 5 or (hour == 5 and minute <= 10):
        base_date = today_date
        base_time = "0200"
    elif hour < 8 or (hour == 8 and minute <= 10): # 5시 11분~8시 10분 사이
        base_date = today_date
        base_time = "0500"
    elif hour<11 or (hour == 11 and minute <=10): # 8시 11분~11시 10분 사이
        base_date = today_date
        base_time = "0800"
    elif hour < 14 or (hour == 14 and minute <= 10): # 11시 11분~14시 10분 사이
        base_date = today_date
        base_time = "1100"
    elif hour < 17 or (hour == 17 and minute <= 10): # 14시 11분~17시 10분 사이
        base_date = today_date
        base_time = "1400"
    elif hour < 20 or (hour == 20 and minute <= 10): # 17시 11분~20시 10분 사이
        base_date = today_date
        base_time ="1700" 
    elif hour < 23 or (hour == 23 and minute <= 10): # 20시 11분~23시 10분 사이
        base_date = today_date
        base_time ="2000"
    else: # 23시 11분~23시 59분
        base_date = today_date
        base_time = "2300"



    # 지금 현재 날씨 정보 제공 내일 출근 날씨 제공 json 정보 불러오기

    params ={'serviceKey' : 'Rty09EbsqEEgCQyDM03L//hEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W/FwB4w==', 
        'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON',
        'base_date' : base_date, 'base_time' : base_time, 'nx' : x, 'ny' : y}


    res = requests.get(url, params=params)

    #json 값에서 item 뽑기

    r_dict = json.loads(res.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_items = r_body.get("items")
    r_item = r_items.get("item")

    # item에 있는 여러 값들 중에 필요한 날씨 데이터 뽑아내기

    # 현재 시간의 날씨 정보 data에 저장
    today = {}
    

    # today에 현재 시간의 날씨 정보 담기(현재 시간을 계산해서 
    # 예보 시각(fcstTime)에 맞는 날씨 정보 담기)
    for item in r_item:
        if(item.get("fcstDate") == today_date and item.get("fcstTime") == str(int(time) // 100 * 100) and item.get("category") == "TMP"):
            today['기온'] = item["fcstValue"] + '℃'

        if(item.get("fcstDate") == today_date and item.get("fcstTime") == str(int(time) // 100 * 100) and item.get("category") == "PTY"):
            rainfall_code = item.get("fcstValue") 

            if rainfall_code == '1':
                rainfall_state = '비'

            elif rainfall_code == '2':
                rainfall_state = '비/눈'

            elif rainfall_code == '3':
                rainfall_state = '눈'

            elif rainfall_code == '4':
                rainfall_state = '소나기'

            else:
                rainfall_state = '없음'

            today['눈/비 소식'] = rainfall_state

        if(item.get("fcstDate") == today_date and item.get("fcstTime") == str(int(time) // 100 * 100) and item.get("category") == "POP"):
            today['강수확률'] = item["fcstValue"] + '%'

        if(item.get("fcstDate") == today_date and item.get("fcstTime") == str(int(time) // 100 * 100) and item.get("category") == "REH"):
            today['습도'] = item["fcstValue"] + '%'

        if(item.get("fcstDate") == today_date and item.get("fcstTime") == str(int(time) // 100 * 100) and item.get("category") == "WSD"):
            today['풍속'] = item["fcstValue"] + 'm/s'

        if(item.get("fcstDate") == today_date and item.get("fcstTime") == str(int(time) // 100 * 100) and item.get("category") == "SKY"):
            weather_code = item.get("fcstValue")

            if weather_code == '1':
                weather_state = '맑음'

            elif weather_code == '3':
                weather_state = '구름많음'

            else:
                weather_state = '흐림'

            today['sky'] = weather_state

   
    today["date"] = today_date

    


    # 다음날 출근 시간(0700)을 기준으로 날씨 정보 받아오기
    tomorrow = {}

    for item in r_item:
        if(item.get("fcstTime") == "0700" and item.get("fcstDate") == tomorrow_date and item.get("category") == "TMP"):
            tomorrow['기온'] = item["fcstValue"] + '℃'

        if(item.get("fcstTime") == "0700" and item.get("fcstDate") == tomorrow_date and item.get("category") == "PTY"):
            rainfall_code = item.get("fcstValue") 

            if rainfall_code == '1':
                rainfall_state = '비'

            elif rainfall_code == '2':
                rainfall_state = '비/눈'

            elif rainfall_code == '3':
                rainfall_state = '눈'

            elif rainfall_code == '4':
                rainfall_state = '소나기'

            else:
                rainfall_state = '없음'

            tomorrow['눈/비 소식'] = rainfall_state

        if(item.get("fcstTime") == "0700" and item.get("fcstDate") == tomorrow_date and item.get("category") == "POP"):
            tomorrow['강수확률'] = item["fcstValue"] + '%'

        if(item.get("fcstTime") == "0700" and item.get("fcstDate") == tomorrow_date and item.get("category") == "REH"):
            tomorrow['습도'] = item["fcstValue"] + '%'

        if(item.get("fcstTime") == "0700" and item.get("fcstDate") == tomorrow_date and item.get("category") == "WSD"):
            tomorrow['풍속'] = item["fcstValue"] + 'm/s'

        if(item.get("fcstTime") == "0700" and item.get("fcstDate") == tomorrow_date and item.get("category") == "SKY"):
            weather_code = item.get("fcstValue")

            if weather_code == '1':
                weather_state = '맑음'

            elif weather_code == '3':
                weather_state = '구름많음'

            else:
                weather_state = '흐림'

            tomorrow['sky'] = weather_state

    
    tomorrow["date"] = tomorrow_date
    

    print(base_date)
    print(base_time)
    print(today)
    print(tomorrow)

    
    # return HttpResponse(res)
    # weather.html로 보내 출력하기
    return render(request, 'weatherapp/weather.html', {'today': today, 'tomorrow':tomorrow})



  