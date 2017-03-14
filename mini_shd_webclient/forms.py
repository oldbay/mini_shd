# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import (
    TextField,
    PasswordField,
    BooleanField,
    FieldList,
    FormField
)


class AuthForm(FlaskForm):
    login = TextField(u'Логин')
    passwd = PasswordField(u'Пароль')
    button = BooleanField(False)


class RegForm(FlaskForm):
    genlogin = TextField(u'Задайте логин')
    passwd = PasswordField(u'Задайте пароль')
    passwd_verifi = PasswordField(u'Повторите пароль')
    button = BooleanField(False)
    rbutton = BooleanField(False)


class RepassForm(FlaskForm):
    passwd = PasswordField(u'Измените пароль')
    button = BooleanField(False)


class MyfilesForm(FlaskForm):
    fname = TextField(u'')
    down = BooleanField(False)
    delit = BooleanField(False)


class MyfilesList(FlaskForm):
    fileslist = FieldList(FormField(MyfilesForm))
