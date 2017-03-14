
# -*- coding: UTF-8 -*-

from md5 import md5
import sys
import os
import unittest


class AllTest(unittest.TestCase):

    def setUp(self):

        self._users = {
            "myuser1": "mypass1",
            "myuser2": "mypass2",
            "myuser3": "mypass3",
            }
        self._files = {
            "myuser1": "file1",
            "myuser2": "file2",
            "myuser3": "file3",
            }
        self._conts = {
            "file1": "myfile content",
            "file2": "myfile content",
            "file3": "myfile new content",
            }

        print
        print "-"*60
        print "Init Database"
        print "-"*60
        # add sys path
        sys.path.append(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        # add test config file
        os.environ["MINI_SHD_CONFIG"] = "%s/test.cfg"%(
            os.path.dirname(os.path.abspath(__file__))
        )
        from mini_shd_server import db_interface
        self.op = db_interface.Operation()

    def test_user(self):
        print
        print "-"*60
        print "TEST: Useradd"
        print "-"*60
        for _user in self._users:
            self.assertTrue(
                self.op.user_add(_user, self._users[_user])
            )
            self.assertTrue(
                self.op.user_query("one", _user).passwd == self._users[_user]
            )
        print
        print "-"*60
        print "TEST: Usermod"
        print "-"*60
        newpass = "blabla"
        for _user in self._users:
            self.assertTrue(
                self.op.user_add(_user, newpass)
            )
            self.assertTrue(
                self.op.user_query("one", _user).passwd == newpass
            )
        print
        print "-"*60
        print "TEST: Userdel"
        print "-"*60
        for _user in self._files:
            # add files for user
            _fname = self._files[_user]
            _cont = self._conts[_fname]
            _md5 = md5(_cont).hexdigest()
            self.assertTrue(
                self.op.file_put(_user, _fname, _cont)
            )
            self.assertTrue(
                self.op.file_query("one", _user, _fname).md5 == _md5
            )
            # remove user and all files
            self.assertTrue(
                self.op.user_del(_user)
            )
            self.assertTrue(
                self.op.file_query("all", _user) == []
            )

    def test_file(self):
        print
        print "-"*60
        print "MODE: Useradd"
        print "-"*60
        for _user in self._users:
            self.assertTrue(
                self.op.user_add(_user, self._users[_user])
            )
            self.assertTrue(
                self.op.user_query("one", _user).passwd == self._users[_user]
            )
        print
        print "-"*60
        print "TEST: Files Put"
        print "-"*60
        for _user in self._files:
            _fname = self._files[_user]
            _cont = self._conts[_fname]
            _md5 = md5(_cont).hexdigest()
            self.assertTrue(
                self.op.file_put(_user, _fname, _cont)
            )
            self.assertTrue(
                self.op.file_query("one", _user, _fname).md5 == _md5
            )
            self.assertIsNotNone(
                self.op.pull_query("first", _md5)
            )
        print
        print "-"*60
        print "TEST: Files Get"
        print "-"*60
        for _user in self._files:
            _fname = self._files[_user]
            _cont = self._conts[_fname]
            self.assertEqual(
                self.op.file_get(_user, _fname), _cont
            )
        print
        print "-"*60
        print "TEST: Files Del"
        print "-"*60
        _user = "myuser1"
        _fname = self._files[_user]
        _cont = self._conts[_fname]
        _md5 = md5(_cont).hexdigest()
        self.assertTrue(
            self.op.file_del(_user, _fname)
        )
        self.assertIsNotNone(
            self.op.pull_query("first", _md5)
        )
        _user = "myuser2"
        _fname = self._files[_user]
        _cont = self._conts[_fname]
        _md5 = md5(_cont).hexdigest()
        self.assertTrue(
            self.op.file_del(_user, _fname)
        )
        self.assertIsNone(
            self.op.pull_query("first", _md5)
        )
        _user = "myuser3"
        _fname = self._files[_user]
        _cont = self._conts[_fname]
        _md5 = md5(_cont).hexdigest()
        self.assertTrue(
            self.op.file_del(_user, _fname)
        )
        self.assertIsNone(
            self.op.pull_query("first", _md5)
        )

if __name__ == "__main__":
    unittest.main()
