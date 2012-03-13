from . import TestCase


class TestSimple(TestCase):
    def test_noop(self):
        """Make sure we don't do anything if not explicitly enabled."""
        raise NotImplementedError()

    def test_trigger_single_path_single_exec(self):
        """Test with a single trigger with a single command."""
        raise NotImplementedError()

    def test_triggers_two_paths_single_exec_each(self):
        """Test with 2 triggers on 2 different paths."""
        raise NotImplementedError()

    def test_triggers_path_subpath_single_exec_each(self):
        """Test triggers on a path and a subpath of it."""
        raise NotImplementedError()
