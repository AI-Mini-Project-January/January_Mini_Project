from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import datetime

def get_weather(request):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    service_key = 'Rty09EbsqEEgCQyDM03L%2F%2FhEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W%2FFwB4wRty09EbsqEEgCQyDM03L//hEwSnSIENiavOyVF3BsZwUSxzkFNKrJFgbXTSayi81l4WbTijUpuHbow5W/FwB4w=='

    today = datetime.datetime.today()
    base_date = today.strftime("%Y%m%d")
    base_time = "0500"

    nx = "62"
    ny = "122"

    params = "serviceKey=" + service_key + "&" +\
        "dataType=json" + "&" +\
        "base_date=" + base_date + "&" +\
        "base_time=" + base_time + "&" +\
        "nx=" + nx + "&" +\
        "ny=" + ny

    res = requests.get(url + params)

    items = res.json().get('response').get('body').get('items')

    # return HttpResponse(items)

