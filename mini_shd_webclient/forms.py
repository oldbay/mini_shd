# -*- coding: UTF-8 -*-

from flask_wtf import Form
from wtforms import (
    TextField,
    PasswordField,
    BooleanField,
    FieldList,
    FormField
)


class AuthForm(Form):
    login = TextField(u'Логин')
    passwd = PasswordField(u'Пароль')
    button = BooleanField(False)


class RegForm(Form):
    genlogin = TextField(u'Задайте логин')
    passwd = PasswordField(u'Задайте пароль')
    passwd_verifi = PasswordField(u'Повторите пароль')
    button = BooleanField(False)
    rbutton = BooleanField(False)


class RepassForm(Form):
    passwd = PasswordField(u'Измените пароль')
    button = BooleanField(False)


class MyfilesForm(Form):
    fname = TextField(u'')
    down = BooleanField(False)
    delit = BooleanField(False)


class MyfilesList(Form):
    fileslist = FieldList(FormField(MyfilesForm))
