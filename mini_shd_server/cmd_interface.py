#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

import settings
from db_interface import Operation


class User():

    """
    Class Uaser
    """

    __dbi = Operation()

    def __init__(self, _name=settings.init["user"], _passwd=settings.init["passwd"]):
        self.name = _name
        self.passwd = _passwd

    def useradd(self):
        _query = self.__dbi.user_query("first", self.name)
        if _query is None:
            return self.__dbi.user_add(self.name, self.passwd)
        else:
            return False

    def auth(self):
        _query = self.__dbi.user_query("first", self.name)
        if _query != None:
            _testpass = str(_query.passwd)
            if self.passwd == _testpass:
                return True
            else:
                return False
        else:
            return False

    def usermod(self, _newpass):
        if self.auth():
            self.passwd = _newpass
            return self.__dbi.user_add(self.name, self.passwd)
        else:
            return False

    def userdel(self):
        if self.auth():
            return self.__dbi.user_del(self.name)
        else:
            return False

    def put_file(self, _fname, _obj):
        if self.auth():
            if len(self.__dbi.file_query("all", self.name)) < settings.FUMax:
                return self.__dbi.file_put(self.name, _fname, _obj)
            else:
                return False
        else:
            return False

    def get_file(self, _fname):
        if self.auth():
            return self.__dbi.file_get(self.name, _fname)
        else:
            return False

    def del_file(self, _fname):
        if self.auth():
            return self.__dbi.file_del(self.name, _fname)
        else:
            return False

    def list_file(self):
        if self.auth():
            files = []
            for _qfile in self.__dbi.file_query("all", self.name):
                files.append(_qfile.name)
            return files
        else:
            return False
