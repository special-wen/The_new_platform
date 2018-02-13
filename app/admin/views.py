from flask_admin import BaseView,expose
from flask_login import current_user
import requests,json
from app.models import User

class Setting(BaseView):
    @expose('/')
    def index(self):
        now_user = User.select().count()
        max_user = requests.get('https://api.xiyoulinux.org/users?'+
                                'access_token='+current_user.access_token+
                                '&per_page=1')
        total = json.loads(max_user.text)['total_count']
        if total>now_user:
            self.flash_user()
        return self.render('admin/setting.html')


    @staticmethod
    def flash_user():
        url = 'https://api.xiyoulinux.org/users?access_token=%s&per_page=%d'
        h = requests.get(url%(current_user.access_token,1))
        total = json.loads(h.text)['total_count']
        h = requests.get(url%(current_user.access_token,total))
        user = json.loads(h.text)['data']
        for i in  user:
            if not User.select().where(User.id==i['id']).first():
                print(i['id'])
                User.create(id=i['id'], username=i['name'],
                            avatar=i['avatar_url'], grade=i['grade'])


