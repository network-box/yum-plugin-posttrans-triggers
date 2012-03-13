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
        raise NotImplementedError()

    def test_triggers_two_paths_single_exec_each(self):
        """Test with 2 triggers on 2 different paths."""
        raise NotImplementedError()

    def test_triggers_path_subpath_single_exec_each(self):
        """Test triggers on a path and a subpath of it."""
        raise NotImplementedError()
