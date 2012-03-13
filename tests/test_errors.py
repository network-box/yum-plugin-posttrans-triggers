from . import TestCase


class TestErrors(TestCase):
    def test_ignore_noexec(self):
        """Make sure we ignore triggers without an exec clause."""
        self._run_yum_test(["install", "plouf"],
                           ["posttrans-triggers: Ignoring path " \
                            "/usr/share/plouf: no 'exec' option found"])

    def test_trigger_exec_errors_out(self):
        """Make sure we print errors in triggered commands."""
        self._run_yum_test(["install", "bidule"],
                           ["posttrans-triggers: /bin/ls: cannot access " \
                             "/path/to/inexistent/file: No such file or " \
                             "directory",
                            "posttrans-triggers: Failed to run command " \
                             "(/bin/ls /path/to/inexistent/file)"])
