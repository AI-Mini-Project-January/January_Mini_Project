from django.shortcuts import render
import requests
import json
import datetime
import urllib
import urllib.request
import math



def get_location(request):
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBf9kIq9ciMUvzAr5neaJRMrlbx7rMZJx0'
    data = {
        'considerIp': True, # 현 IP로 데이터 추출
    }

    result = requests.post(url, data) # 해당 API에 요청을 보내며 데이터를 추출한다.
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
    XO = 43     ##  기준점 X좌표
    YO = 136     ##  기준점 Y좌표
    DEGRAD = math.pi / 180.0
    RADDEG = 180.0 / math.pi

    re = Re / grid
    slat1 = slat1 * DEGRAD  #표준위도1
    slat2 = slat2 * DEGRAD  #표준위도2
    olon = olon * DEGRAD    #기준점 경도
    olat = olat * DEGRAD    #기준점 위도

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)  #
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)  #
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)   #
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
    #x좌표, y좌표 리턴
    return x, y


def get_weather(request):
    lat, lng = get_location(request)
    x, y = grid(lat, lng)

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    today = datetime.datetime.today()
    base_date = today.strftime("%Y%m%d")
    base_time = "1700"
    params ={'serviceKey' : 'Rty09EbsqEEgCQyDM03L//hEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W/FwB4w==', 
        'pageNo' : '1', 'numOfRows' : '50', 'dataType' : 'JSON',
        'base_date' : base_date, 'base_time' : base_time, 'nx' : x, 'ny' : y}

    res = requests.get(url, params=params)

    #json 값에서 item 뽑기

    r_dict = json.loads(res.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_items = r_body.get("items")
    r_item = r_items.get("item")

    #item에 있는 여러 값들 중에 
    #필요한 날씨 데이터 뽑아내기

    data = {}

    for item in r_item:
        if(item.get("category") == "TMP"):
            data['기온'] = item["fcstValue"] + '℃'

        if(item.get("category") == "PTY"):
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

            data['눈/비 소식'] = rainfall_state

        if(item.get("category") == "POP"):
            data['강수확률'] = item["fcstValue"] + '%'

        if(item.get("category") == "REH"):
            data['습도'] = item["fcstValue"] + '%'

        if(item.get("category") == "WSD"):
            data['풍속'] = item["fcstValue"] + 'm/s'

        if(item.get("category") == "SKY"):
            weather_code = item.get("fcstValue")

            if weather_code == '1':
                weather_state = '맑음'

            elif weather_code == '3':
                weather_state = '구름많음'

            else:
                weather_state = '흐림'

            data['sky'] = weather_state

    tmp = data['기온']
    wsd = data['풍속']
    sky = data['sky']
    pty = data['눈/비 소식']
    pop = data['강수확률']
    reh = data['습도']

    #result 딕셔너리에 값 저장하고 weather.html로 보내 출력하기

    result = []
    result.append(tmp)
    result.append(wsd)
    result.append(sky)
    result.append(pty)
    result.append(pop)
    result.append(reh)

    return render(request, 'weatherapp/weather.html', {'data':result})
