from . import TestCase


class TestSimple(TestCase):
    def test_noop(self):
        """Make sure we don't do anything if not explicitly enabled."""
        # Don't enable the plugin
        arg = self.default_cmd.pop()
        self.assertEqual(arg, "--posttrans-triggers")

        self._run_yum_test(["install", "foo"],
                           ["posttrans-triggers: Got trigger on path " \
                            "/usr/share/foo (file is " \
                            "/usr/share/foo/some_resource)"],
                           check_in=False)

    def test_trigger_single_path_single_exec(self):
        """Test with a single trigger with a single command."""
        self._run_yum_test(["install", "foo"],
                           ["posttrans-triggers: Got trigger on path " \
                            "/usr/share/foo (file is " \
                            "/usr/share/foo/some_resource)"])

    def test_triggers_two_paths_single_exec_each(self):
        """Test with 2 triggers on 2 different paths."""
        self._run_yum_test(["install", "foo", "bar"],
                           ["posttrans-triggers: Got trigger on path " \
                             "/usr/share/foo (file is " \
                             "/usr/share/foo/some_resource)",
                            "posttrans-triggers: Got trigger on path " \
                             "/usr/share/bar (file is " \
                             "/usr/share/bar/some_resource)"])

    def test_triggers_path_subpath_single_exec_each(self):
        """Test triggers on a path and a subpath of it."""
        self._run_yum_test(["install", "toto"],
                           ["posttrans-triggers: Got trigger on path " \
                             "/usr/share (file is " \
                             "/usr/share/toto/some_resource)",
                            "posttrans-triggers: Got trigger on path " \
                             "/usr/share/toto (file is " \
                             "/usr/share/toto/some_resource)"])

    def test_trigger_on_path_including_libarch(self):
        """Test that %(libarch) is properly replaced in the path before matching."""
        expected_lines = ["posttrans-triggers: Got trigger on path using libarch"]

        self._run_yum_test(["install", "baz"],
                           expected_lines)

    def test_trigger_after_obsoletion(self):
        """Test that we don't fail on now obsoleted packages."""
        # Trick yum to be able to install that obsoleted package
        expected_lines = ["posttrans-triggers: Got trigger on path " \
                           "/usr/share/foo (file is " \
                           "/usr/share/foo/some_resource)"]
        self._run_yum_test(["--exclude=foo2", "install", "foo"], expected_lines)

        # Now run the update to obsolete it
        expected_lines = ["posttrans-triggers: Got trigger on obsolete path " \
                           "/usr/share/foo/ (file is " \
                           "/usr/share/foo/some_resource)",
                          "posttrans-triggers: Got trigger on new path " \
                           "/usr/share/foo2/ (file is " \
                           "/usr/share/foo2/some_resource)"]
        unexpected_lines = ["posttrans-triggers: Got trigger on path " \
                             "/usr/share/foo (file is " \
                             "/usr/share/foo/some_resource)"]
        output = self._run_yum_test(["update"], expected_lines)

        for line in unexpected_lines:
            self.assertTrue(line not in output, output)
