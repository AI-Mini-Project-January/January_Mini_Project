import requests
import json

# # Create your views here.

# #API 토큰 발급
url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '5d03e24af9d6c95a6f526e3308d8879d'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'ktW_n_7c5fPb2mVJNE6q73rMu1ogy7LJs5RtItCWEVjqVB1nrpDq3aSdxewr_hVVVqgx1QorDKYAAAF-gQM9Yg'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# # json 저장
with open(r"C:\Users\User\Desktop\JanuaryProject\kakaoproject\kakao_code.json","w") as fp:
    json.dump(tokens, fp)

with open(r"C:C:\Users\User\Desktop\JanuaryProject\kakaoproject\kakao_code.json","r") as fp:
    ts = json.load(fp)
print(ts)
print(ts["access_token"])
