import requests
import json

#1.
with open(r"C:\Users\User\Desktop\JanuaryProject\kakaoproject\kakao_code.json","r") as fp:
    tokens = json.load(fp)

url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

# kapi.kakao.com/v2/api/talk/memo/default/send 

headers={
    "Authorization" : "Bearer " + tokens["access_token"]
}

data={
    "template_object": json.dumps({
        "object_type":"text",
        "text":"Hello, world!",
        "link":{
            "web_url":"www.naver.com"
        }
    })
}

response = requests.post(url, headers=headers, data=data)
response.status_code