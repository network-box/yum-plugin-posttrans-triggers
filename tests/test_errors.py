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

    def test_trigger_exec_errors_out_at_all_times(self):
        """Make sure we print errors in triggered commands no matter what."""
        # Don't print the regular output, we want to check if errors are still there
        self.default_cmd.remove("--posttrans-triggers-print-output")
        self.assertFalse("--posttrans-triggers-print-output" in self.default_cmd)

        self._run_yum_test(["install", "bidule"],
                           ["posttrans-triggers: /bin/ls: cannot access " \
                             "/path/to/inexistent/file: No such file or " \
                             "directory",
                            "posttrans-triggers: Failed to run command " \
                             "(/bin/ls /path/to/inexistent/file)"])
