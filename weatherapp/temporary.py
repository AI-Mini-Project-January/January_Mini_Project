import json 
from datetime import datetime 
from urllib.request import urlopen


def get_sky_info(data): 
    try: 
        weather_info = data['response']['body']['items']['item'] 
        if weather_info[3]['category'] == 'SKY': 
            return weather_info[3]['fcstValue'] 
        elif weather_info[5]['category'] == 'SKY': 
            return weather_info[5]['fcstValue'] 
    except KeyError: 
        print('API 호출 실패!')


def get_base_time(hour): 
    hour = int(hour) 
    if hour < 3: 
        temp_hour = '20' 
    elif hour < 6: 
        temp_hour = '23' 
    elif hour < 9: 
        temp_hour = '02' 
    elif hour < 12: 
        temp_hour = '05' 
    elif hour < 15: 
        temp_hour = '08' 
    elif hour < 18: 
        temp_hour = '11' 
    elif hour < 21: 
        temp_hour = '14' 
    elif hour < 24: 
        temp_hour = '17' 

    return temp_hour + '00'


def get_weather(): 
    service_key = 'Rty09EbsqEEgCQyDM03L//hEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W/FwB4w==' 
    now = datetime.now() 
    now_date = now.strftime('%Y%m%d') 
    now_hour = int(now.strftime('%H'))


    if now_hour < 6: 
        base_date = str(int(now_date) - 1) 
    else: 
        base_date = now_date 
    base_hour = get_base_time(now_hour)


    num_of_rows = '6' 
    base_date = base_date 
    base_time = base_hour 
    nx = str(60) 
    ny = str(125) 
    _type = 'json'

    api_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={Rty09EbsqEEgCQyDM03L//hEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W/FwB4w==}','&base_date={}&base_time={}&nx={}&ny={}&numOfRows={}&_type={}'.format( service_key, base_date, base_time, nx, ny, num_of_rows, _type)



    data = urlopen(api_url).read().decode('utf8') 
    json_data = json.loads(data) 
    sky = get_sky_info(json_data) 
    return sky

weather = get_weather()
print(weather)







