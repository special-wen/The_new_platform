#coding=utf-8
from flask_admin.contrib.peewee import ModelView

class UserAdmin(ModelView):
    can_create = False
    can_delete = False
    #can_edit = False

    column_display_pk = True
    #设置不可见列
    column_exclude_list = ['access_token','avatar']

    #设置列显示名
    column_labels = dict(username='姓名', grade='年级', power='管理员')

    #可排序列,username通过id排序
    column_sortable_list = (('username','id'),'grade')

    #全文搜索
    #column_searchable_list = ('username','username')

    column_descriptions = dict(
        power='拥有该权限的人才能访问后台'
    )

    column_filters = ('power','grade','username')


    #设置可在列表中编辑的列
    column_editable_list = ('power')

    #设置表单不显示的列
    form_excluded_columns = ('access_token','avatar')

    #设置一些样式
    form_widget_args = {
        'username': {
            'disabled': True
        },
        'grade':{
            'disabled':True
        },
    }

class InterAdmin(ModelView):
    column_display_pk = True

class RecordAdmin(ModelView):
    column_display_pk = True


