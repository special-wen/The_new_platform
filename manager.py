#coding=utf-8
import os
from flask_script import Manager
from app import create_app
from flask_admin import Admin
from app.admin.views import Setting
from flask_babelex import Babel
from app.models import User,Interviewer,Record


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
admin = Admin(app,name='后台管理',template_mode='bootstrap3')
babel = Babel(app)



def create_all_tables():
    models = [User,Interviewer,Record]
    for model in models:
        model.create_table(fail_silently=True)
from app.admin.modelviews import UserAdmin,InterAdmin,RecordAdmin

if __name__=='__main__':
    create_all_tables()
    admin.add_view(Setting(name='设置', url='/admin/settings'))
    admin.add_view(UserAdmin(User,name='成员管理'))
    admin.add_view(InterAdmin(Interviewer,name='面试者管理'))
    admin.add_view(RecordAdmin(Record,name='面试记录管理'))
    manager.run()