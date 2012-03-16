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

    def test_filelist_from_network(self):
        """Make sure we get the file list from the repo when it's not in the RPM DB."""
        # This test is somewhat bizarre. So far, I've only experienced the
        # "problem" when obsoleting a package that was declared as
        # "installonly" in the configuration file.
        # -- So first, let's declare a package as installonly ----------------
        with open(self.yumconf, "r") as input:
            with open(self.yumconf+".tmp", "w") as output:
                for line in input:
                    output.write(line)
                    if line.startswith("installroot="):
                        # It was the last line of the global conf, add one more
                        output.write("installonlypkgs=foo\n")
        import os
        os.rename(self.yumconf+".tmp", self.yumconf)

        # -- Now redo the obsoletion test, since that triggers the issue -----
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
