# coding=utf-8
from flask import Flask
from config import config
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.index'
#登陆提示信息
login_manager.login_message=u'对不起，您还没有登录'
login_manager.login_message_category='info'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)

    # 附加基本路由
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 附加通用api路由
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # 附加权限验证路由
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='')

    return app
