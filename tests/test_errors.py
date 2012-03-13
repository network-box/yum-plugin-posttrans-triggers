from . import TestCase


class TestErrors(TestCase):
    def test_ignore_noexec(self):
        """Make sure we ignore triggers without an exec clause."""
        raise NotImplementedError()

    def test_trigger_exec_errors_out(self):
        """Make sure we print errors in triggered commands."""
        raise NotImplementedError()
