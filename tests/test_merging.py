from . import TestCase


class TestMerging(TestCase):
    def test_multiple_triggers_same_path(self):
        """Make sure we run all triggers on the same path."""
        self._run_yum_test(["install", "foo", "foo-addons"],
                           ["posttrans-triggers: Got trigger on path " \
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
                             "/usr/share/foo/some_other_resource)"])

    def test_single_trigger_multiple_exec(self):
        """Make sure we run all exec commands for a given path."""
        raise NotImplementedError()

    def test_multiple_trigger_same_exec(self):
        """Make sure we run a given trigger command only once."""
        raise NotImplementedError()
