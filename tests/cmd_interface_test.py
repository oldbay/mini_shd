
# -*- coding: UTF-8 -*-

import sys
import os
import filecmp
import unittest


class AllTest(unittest.TestCase):

    def setUp(self):

        self._inupt_file = "%s/test.jpg"%(
            os.path.dirname(os.path.abspath(__file__))
        )
        self._output_file = "/tmp/mini_shd_test_output.jpg"

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
        from mini_shd_server import cmd_interface
        self.user = cmd_interface.User("myuser", "mypass")

    def tearDown(self):

        if self._output_file in os.path.dirname(os.path.abspath(self._output_file)):
            os.remove("/tmp/mini_shd_test_output.jpg")

    def test_all(self):
        print
        print "-"*60
        print "TEST: Useradd"
        print "-"*60
        self.assertTrue(
            self.user.useradd()
        )
        self.assertTrue(
            self.user.auth()
        )
        print
        print "-"*60
        print "TEST: Usermod"
        print "-"*60
        self.assertTrue(
            self.user.usermod("newpass")
        )
        self.assertTrue(
            self.user.auth()
        )
        print
        print "-"*60
        print "TEST: Put File"
        print "-"*60
        inp = open(self._inupt_file, "rb")
        _input_obj = inp.read()
        inp.close()
        _filename = "myfile"
        self.assertTrue(
            self.user.put_file(_filename, _input_obj)
        )
        self.assertIn(
            _filename, self.user.list_file()
        )
        print
        print "-"*60
        print "TEST: Add put two File"
        print "-"*60
        inp = open(self._inupt_file, "rb")
        _input_obj = inp.read()
        inp.close()
        _filename_new = "myfile_new"
        self.assertFalse(
            self.user.put_file(_filename_new, _input_obj)
        )
        print
        print "-"*60
        print "TEST: Get File"
        print "-"*60
        _output_obj = self.user.get_file(_filename)
        out = open(self._output_file, "wb")
        out.write(_output_obj)
        out.close()
        self.assertTrue(
            filecmp.cmp(self._inupt_file, self._output_file)
        )
        print
        print "-"*60
        print "TEST: Del File"
        print "-"*60
        self.assertTrue(
            self.user.del_file(_filename)
        )
        self.assertNotIn(
            _filename, self.user.list_file()
        )
        print
        print "-"*60
        print "TEST: Userdel"
        print "-"*60
        self.assertTrue(
            self.user.userdel()
        )
        self.assertFalse(
            self.user.auth()
        )


if __name__ == "__main__":
    unittest.main()
