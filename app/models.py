# coding=utf-8
from peewee import *
import datetime
from flask_login import UserMixin
from . import login_manager
import os
from config import BASE_DIR


db = SqliteDatabase(BASE_DIR+'/sqlite.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(UserMixin,BaseModel):

    username = CharField()
    access_token = CharField(null=True)
    power = BooleanField(default=False)
    avatar = CharField(null=True)
    grade = CharField(null=True)


    def to_json(self):
        json_data = {
            'id':self.id,
            'name':self.username,
            'power':self.power,
            'avatar':self.avatar if self.avatar else "",
            'grade':self.grade
        }
        return json_data

    def __repr__(self):
        return '<小组成员 %s>' % (self.username)

    def is_superuser(self):
        return True if self.power else False


class AnonymousUser():
    @property
    def is_anonymous(self):
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id == int(user_id)).first()

class Interviewer(BaseModel):
    name = CharField(max_length=128)
    grade = SmallIntegerField() #几年级
    stu_num = CharField(max_length=16)
    classes = CharField(max_length=5) #20××年面试
    sex = BooleanField(default=True) #True为男
    is_alive = BooleanField(default=False,help_text='是否面试')

    def to_json(self):
        json_data = {
            'id':self.id,
            'name':self.name,
            'sex':self.sex,
            'num':self.stu_num,
            'grade':self.grade,
            'classes':self.classes,
        }
        return json_data

    def __repr__(self):
        return '<面试者  %s>' % (self.name)

class Record(BaseModel):
    interviewer = ForeignKeyField(Interviewer)
    data = DateTimeField(default=datetime.datetime.now)
    is_power = BooleanField(default=False,help_text='大轮综合评定')
    big_num = CharField(help_text='大轮数')
    sml_num = SmallIntegerField(help_text='小轮数',null=True)
    good = TextField(help_text='优点',null=True)
    bad = TextField(help_text='缺点',null=True)
    score = SmallIntegerField(help_text='90-100:SS、80-89:S、70-79:A、60-69:B、50-59:C、50以下:D') #评分
    leader = ForeignKeyField(User)
    others = TextField(help_text='组员，保存id序列',null=True)

    def to_json(self):
        others = ''
        for i in self.othres.split():
            u = User.select().where(id=int(i)).first()
            others = others + '??? ' if not u else u.username+' '
        json_data = {
            'owner':self.interviewer.name,
            'time':self.data,
            'power':self.is_power,
            'big':self.big_num,
            'sml':self.sml_num,
            'good':self.good,
            'bad':self.bad,
            'score':self.score,
            'leader':self.leader.username,
            'others':others
        }
        return json_data