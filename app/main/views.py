#coding=utf-8
from . import main
from flask import render_template,current_app,redirect
from app.auth.views import Get_Auth
from flask_login import login_required,current_user


@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@main.route('/')
def index():
    return render_template('base.html')


@main.route('/login')
def login():
    return redirect(Get_Auth())


@main.route('/sign_in')
@login_required
def sign_in():
    return render_template('sign_in.html')