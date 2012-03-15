from . import TestCase


class TestMultiSteps(TestCase):
    def test_trigger_after_obsoletion(self):
        """Test that we don't fail on now obsoleted packages."""
        # Trick yum to be able to install that obsoleted package
        expected_lines = ["posttrans-triggers: Got trigger on path " \
                           "/usr/share/foo (file is " \
                           "/usr/share/foo/some_resource)"]
        self._run_yum_test(["--exclude=foo2", "install", "foo"],
                           expected=expected_lines)

        # Now run the update to obsolete it
        unexpected_lines = expected_lines[:]
        expected_lines = ["posttrans-triggers: Got trigger on obsolete path " \
                           "/usr/share/foo/ (file is " \
                           "/usr/share/foo/some_resource)",
                          "posttrans-triggers: Got trigger on new path " \
                           "/usr/share/foo2/ (file is " \
                           "/usr/share/foo2/some_resource)"]
        self._run_yum_test(["update"], expected=expected_lines,
                           unexpected=unexpected_lines)

    def test_trigger_after_update(self):
        """Test that we don't fail on now updated packages."""
        # Trick yum to be able to install that updated package
        import glob
        old_pkg = glob.glob("%s/foo-1-1*.rpm" % self.testrepo_baseurl)[0]

        expected_lines = ["posttrans-triggers: Got trigger on path " \
                           "/usr/share/foo (file is " \
                           "/usr/share/foo/some_resource)"]
        self._run_yum_test(["--disablerepo=*", "install", old_pkg],
                           expected=expected_lines)

        # Now run the update to obsolete it
        unexpected_lines = expected_lines[:]
        expected_lines = ["posttrans-triggers: Got trigger on old path " \
                           "/usr/share/foo/ (file is " \
                           "/usr/share/foo/some_resource)",
                          "posttrans-triggers: Got trigger on new path " \
                           "/usr/share/foo-2/ (file is " \
                           "/usr/share/foo-2/some_resource)"]
        self._run_yum_test(["update"], expected=expected_lines,
                           unexpected=unexpected_lines)
