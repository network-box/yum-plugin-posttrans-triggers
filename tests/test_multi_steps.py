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

    def test_trigger_after_removal(self):
        """Test that we don't fail on now removed packages."""
        # First install two packages providing different triggers on the same
        # path (this is from TestMerging.test_multiple_triggers_same_path()
        expected_lines = ["posttrans-triggers: Got trigger on path " \
                            "/usr/share/foo (file is " \
                            "/usr/share/foo/some_resource)",
                          "posttrans-triggers: Got trigger on path " \
                            "/usr/share/foo (file is " \
                            "/usr/share/foo/some_other_resource)",
                          "posttrans-triggers: Got addons trigger on path " \
                            "/usr/share/foo (file is " \
                            "/usr/share/foo/some_resource)",
                          "posttrans-triggers: Got addons trigger on path " \
                            "/usr/share/foo (file is " \
                            "/usr/share/foo/some_other_resource)"]
        self._run_yum_test(["install", "foo", "foo-addons"],
                           expected=expected_lines)

        # Now comes the actual test: remove 'foo-addons', and observe the
        # trigger from 'foo' being run for the removed files in 'foo-addons'
        expected_lines = ["posttrans-triggers: Got trigger on path " \
                            "/usr/share/foo (file is " \
                            "/usr/share/foo/some_other_resource)"]
        self._run_yum_test(["remove", "foo-addons"], expected=expected_lines)
