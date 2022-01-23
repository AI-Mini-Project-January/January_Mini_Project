from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
import json
import datetime
import pandas as pd
import urllib
import urllib.request
from bs4 import BeautifulSoup

def static(request):
    return render(request, 'weatherapp/weather.html')

# 날씨 출력 
def get_weather(request):
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

    today = datetime.datetime.today()
    base_date = today.strftime("%Y%m%d")
    base_time = "0800"

    


    

    params ={'serviceKey' : 'Rty09EbsqEEgCQyDM03L//hEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W/FwB4w==', 
        'pageNo' : '1', 'numOfRows' : '50', 'dataType' : 'JSON', 
        'base_date' : base_date, 'base_time' : base_time, 'nx' : '62', 'ny' : '122'}


    res = requests.get(url, params=params)

    # return HttpResponse(res)
    print("=== response json data start ===")
    print(res.text)
    print("=== response json data end ===")
    print()

    r_dict = json.loads(res.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_items = r_body.get("items")
    r_item = r_items.get("item")
    

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

            data['날씨'] = weather_state

    
    return JsonResponse(data)




# ServiceKey = 'Rty09EbsqEEgCQyDM03L//hEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W/FwB4w=='

# url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

# queryParams = '?' + urllib.parse.urlencode(
#     {
#         urllib.parse.quote_plus('ServiceKey') : ServiceKey, # key를 바로 입력해도 됩니다.
#         urllib.parse.quote_plus('numOfRows') : '113', # 총 14개의 항목을 3시간 단위로 순차적으로 불러옵니다. 다음날 24시간예보에 필요한 만큼만 가져왔습니다.
#         urllib.parse.quote_plus('dataType') : 'JSON', # JSON, XML 두가지 포멧을 제공합니다.
#         urllib.parse.quote_plus('base_date') : '20220123', # 예보 받을 날짜를 입력합니다. 최근 1일간의 자료만 제공합니다.
#         urllib.parse.quote_plus('base_time') : '0200', # 예보 시간을 입력합니다. 2시부터 시작하여 3시간 단위로 입력 가능합니다.
#         urllib.parse.quote_plus('nx') : '62', # 울산 태양광 발전소 x 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
#         urllib.parse.quote_plus('ny') : '122' # 울산 태양광 발전소 y 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
#     }
# )

# response = urllib.request.urlopen(url + queryParams).read()
# response = json.loads(response)

# fcst_df = pd.DataFrame()
# date = '2022-01-23'
# fcst_df['Forecast_time'] = [f'{date} {hour}:00' for hour in range(24)]
# row_idx = 0

# for i, data in enumerate(response['response']['body']['items']['item']):
#     if i > 19:
#         if data['category']=='REH':
#             fcst_df.loc[row_idx, 'Humidity'] = float(data['fcstValue'])
#             print('category:Humidity,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
#         elif data['category']=='T3H':
#             fcst_df.loc[row_idx, 'Temperature'] = float(data['fcstValue'])
#             print('category:Temperature,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
#         elif data['category']=='SKY':
#             fcst_df.loc[row_idx, 'Cloud'] = float(data['fcstValue'])
#             print('category:Cloud,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
#         elif data['category']=='VEC':
#             fcst_df.loc[row_idx, 'WindDirection'] = float(data['fcstValue'])
#             print('category:WindDirection,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
#         elif data['category']=='WSD':
#             fcst_df.loc[row_idx, 'WindSpeed'] = float(data['fcstValue'])
#             print('category:WindSpeed,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'], '\n')
#             row_idx+=3





    




    #미세먼지 api
    # url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
    # params ={'serviceKey' : 'Rty09EbsqEEgCQyDM03L//hEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W/FwB4w==', 'returnType' : 'json', 'numOfRows' : '100', 'pageNo' : '10', 'searchDate' : '2022-01-23', 'InformCode' : 'PM10' }

    # result = requests.get(url, params=params)
    # print(result.text)
    # result2 = json.loads(result.text)
    # r_item = result2.get("item")

    # print(r_item)



    # response = requests.get(url, params=params)
    
    # r_dict = json.loads(response.text)
    # r_response = r_dict.get("response")
    # r_body = r_response.get("body")
    # r_items = r_body.get("items")
    # r_item = r_items.get("item")

    # result = {}
    # for item in r_item:
    #         if(item.get("category") == "T1H"):
    #                 result = item
    #                 break
    # for item in r_item:
    #         if(item.get("category") == "RN1"):
    #                 result2 = item
    #                 break


    # print("=== response dictionary(python object) data start ===")
    # print(result.get("baseTime")[:-2] +" temp : " + result.get("fcstValue") + "C")
    # print(result2.get("baseTime")[:-2] +" rain : " + result2.get("fcstValue") + "mm")
    # print("=== response dictionary(python object) data end ===")
    # print()
    




    

# 위,경도 정보 격자로 변환
import math
NX = 149            ## X축 격자점 수
NY = 253            ## Y축 격자점 수

Re = 6371.00877     ##  지도반경
grid = 5.0          ##  격자간격 (km)
slat1 = 30.0        ##  표준위도 1
slat2 = 60.0        ##  표준위도 2
olon = 126.0        ##  기준점 경도
olat = 38.0         ##  기준점 위도
xo = 210 / grid     ##  기준점 X좌표
yo = 675 / grid     ##  기준점 Y좌표
first = 0

if first == 0 :
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI/ 180.0
    RADDEG = 180.0 / PI


    re = Re / grid
    slat1 = slat1 * DEGRAD
    slat2 = slat2 * DEGRAD
    olon = olon * DEGRAD
    olat = olat * DEGRAD

    sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(PI * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(PI * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    first = 1




def mapToGrid(lat, lon, code = 0 ):
    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI :
        theta -= 2.0 * PI
    if theta < -PI :
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    return x, y







