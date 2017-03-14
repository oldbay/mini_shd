#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

from settings import init

from md5 import md5
from sqlalchemy.orm import sessionmaker
from model import engine, Pull, File, User


class Database(object):

    """
    Connect to database and return a Session object
    """

    def connect(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session


class Operation(object):

    """
    Database operations
    query - use qtype=(all,one,first)
    """

    def __init__(self):
        self.__session = Database().connect()

    def __del__(self):
        self.__session.close()

    def user_query(self, _qtype, _name=False, _passwd=False):
        query = self.__session.query(User)
        if _name:
            query = query.filter_by(name=u""+_name)
        if _passwd:
            query = query.filter_by(passwd=u""+_passwd)
        if _qtype == "all":
            return query.all()
        elif _qtype == "one":
            return query.one()
        elif _qtype == "first":
            return query.first()

    def user_add(self,
                 _name=init["user"],
                 _passwd=init["passwd"]
                 ):
        _query = self.user_query("first", _name)
        if _query is None:
            add_row = User()
            add_row.name = u""+_name
            add_row.passwd = u""+_passwd
            self.__session.add(add_row)
            self.__session.commit()
            _query = self.user_query("one", _name)
        else:
            _query.passwd = u""+_passwd
            self.__session.commit()
        return _query.id

    def user_del(self, _name):
        _query = self.user_query("one", _name)
        if _query is not None:
            # delete files of user
            self.file_del(_query.name)
            # delete user
            self.__session.delete(_query)
            self.__session.commit()
            return True
        else:
            return False

    def file_query(self, _qtype, _uname=False, _fname=False, _md5=False):
        query = self.__session.query(File)
        if _uname:
            query = query.filter_by(uname=u""+_uname)
        if _fname:
            query = query.filter_by(name=u""+_fname)
        if _md5:
            query = query.filter_by(md5=u""+_md5)
        if _qtype == "all":
            return query.all()
        elif _qtype == "one":
            return query.one()
        elif _qtype == "first":
            return query.first()

    def file_put(self, _uname, _fname, _obj):
        _query = self.file_query("first", _uname, _fname)
        if _query is None:
            add_row = File()
            add_row.name = u""+_fname
            add_row.pull_id = self.pull_add(_obj)
            add_row.user_id = self.user_query("one", _uname).id
            self.__session.add(add_row)
            self.__session.commit()
            return True
        else:
            return False

    def file_get(self, _uname, _fname):
        _query = self.file_query("one", _uname, _fname)
        if _query is not None:
            return _query.obj
        else:
            return False

    def file_del(self, _uname, _fname=False):
        _query = self.file_query("all", _uname, _fname)
        if _query != []:
            for _q in _query:
                _md5 = _q.md5
                self.__session.delete(_q)
                self.__session.commit()
                self.pull_del(_md5)
            return True
        else:
            return False

    def pull_query(self, _qtype, _md5):
        query = self.__session.query(Pull)
        query = query.filter_by(md5=u""+_md5)
        if _qtype == "all":
            return query.all()
        elif _qtype == "one":
            return query.one()
        elif _qtype == "first":
            return query.first()

    def pull_add(self, _obj):
        _md5 = md5(_obj).hexdigest()
        _query = self.pull_query("first", _md5)
        if _query is None:
            add_row = Pull()
            add_row.md5 = u""+_md5
            add_row.obj = _obj
            self.__session.add(add_row)
            self.__session.commit()
            _query = self.pull_query("one", _md5)
        return _query.id

    def pull_del(self, _md5):
        _query = self.pull_query("one", _md5)
        if _query is not None:
            if _query.files == []:
                self.__session.delete(_query)
                self.__session.commit()
                return True
            else:
                return False
        else:
            return False
