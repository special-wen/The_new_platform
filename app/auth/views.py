#coding=utf-8
import requests,json
from flask import request,jsonify,current_app,redirect,url_for
from config import Config
from . import auth
from app.models import User
from flask_login import login_user,logout_user,current_user


#构造用户登陆页面
def Get_Auth():
    url = 'https://sso.xiyoulinux.org/oauth/authorize?'
    data = {
        'response_type':'code',
        'client_id':'spider',
        'redirect_uri':'http://localhost:8080/login/',
        'state':current_app.config['AUTH_STATE'],
        'scope':'all'
    }
    for k,v in data.items():
        url = url + '%s=%s&' %(k,v)
    url = url[:-1]
    return url

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

#保存一条新记录
def save_user_message(user,ac):
    u = User.create(id = user.get('id'),username=user.get('name'),grade=user.get('grade'),
                    access_token = ac,avatar = user.get('avatar'))
    return u


@auth.route('/login/')
def login():
    state = request.args.get('state')
    if state != Config.AUTH_STATE:
        #csrf attack?
        return jsonify({'code':'error'}),401

    code = request.args.get('code')
    (at,ei) = Get_AccessToken(code)
    if not at or not ei:
        return jsonify({'code': 'error'}), 401

    user = Get_User_message(at)
    u = User.select().where(User.id == user.get('id')).first()
    if not u:
        #保存用户记录
        u = save_user_message(user,at)
    else:
        # 修改用户记录
        u.access_token = at
        u.save()
    login_user(u)
    return redirect(url_for('main.index'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect('https://sso.xiyoulinux.org/logout')
