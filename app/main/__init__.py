#coidng=utf-8
import requests, json
from flask import Blueprint

main = Blueprint('main',__name__)

from . import views

#获取到用户的access token
def Get_AccessToken(authcode):
    url = 'https://sso.xiyoulinux.org/oauth/access_token'
    data = {
        'grant_type':'authorization_code',
        'client_id':'spider',
        'client_secret':'$2y$10$OmNWVGJLqsCAbHELzg4VwezzT/94Jpn3J',
        'code':authcode,
        'redirect_uri':'http://localhost:8080/login/'
    }
    try:
        html = requests.post(url,data=data)
        js = json.loads(html.text)
        at = js.get('access_token')
        ei = js.get('expires_in')
        return (at,ei)
    except Exception as e:
        print(e)
    return (None,None)

#获取用户信息
def Get_User_message(access_token):
    url = 'https://api.xiyoulinux.org/me?access_token=%s' % access_token
    html = requests.get(url)
    user = json.loads(html.text)
    return user
