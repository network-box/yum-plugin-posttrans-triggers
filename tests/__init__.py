import os
import subprocess
import unittest


global_dataroot = os.path.join(os.path.abspath(os.getcwd()), "tests/data")
conf_template = "/etc/yum.conf"


class TestCase(unittest.TestCase):
    def setUp(self):
        # -- A few useful definitions ------------------------------
        self.dataroot = os.path.join(global_dataroot, self.__class__.__name__)
        self.yumconf = os.path.join(self.dataroot,
                                    "%s.conf" % self._testMethodName)
        self.installroot = os.path.join(self.dataroot,
                                        "%s.root" % self._testMethodName)
        self.testrepo_baseurl = os.path.join(self.dataroot,
                                             "%s.repo" % self._testMethodName)

        self.default_cmd = ["/usr/bin/yum", "-y", "-c", self.yumconf,
                            "--posttrans-triggers"]

        # -- Write the yum config and test repo --------------------
        with open(conf_template, "r") as input:
            with open(self.yumconf, "w") as output:
                for line in input.readlines():
                    output.write(line)

                output.write("installroot=%s\n" % self.installroot)
                output.write("\n")
                output.write("[test]\n")
                output.write("name=Test repo\n")
                output.write("enabled=1\n")
                output.write("baseurl=file://%s\n" % self.testrepo_baseurl)
                output.write("gpgcheck=0\n")

    def tearDown(self):
        cmd = ["/usr/bin/yum", "-c", self.yumconf, "clean", "all"]
        subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        cmd = ["/bin/rm", "-fr", self.yumconf, self.installroot,
               ]
        subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def _run_yum_test(self, args, expected=None, unexpected=None):
        """This is not a test method, just a helper to avoid duplication."""
        if expected is None:
            expected = []
        if unexpected is None:
            unexpected = []

        fail_msg = "%s line:\n    %s\nIs %sin the output:\n    %s"

        cmd = self.default_cmd + args
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, unused = proc.communicate()
        result = stdout.split("\n")

        for line in expected:
            self.assertTrue(line in result,
                            msg=(fail_msg % ("Expected", line, "not ",
                                             "\n    ".join(result))))
        for line in unexpected:
            self.assertTrue(line not in result,
                            msg=(fail_msg % ("Unexpected", line, "",
                                             "\n    ".join(result))))

        return result


from .test_simple import *
from .test_errors import *
from .test_merging import *
from .test_multi_steps import *
