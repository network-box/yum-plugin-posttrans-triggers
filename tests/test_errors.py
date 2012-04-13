from . import TestCase


class TestErrors(TestCase):
    def test_ignore_noexec(self):
        """Make sure we ignore triggers without an exec clause."""
        expected_lines = ["posttrans-triggers: Ignoring path " \
                            "/usr/share/plouf: no 'exec' option found"]
        self._run_yum_test(["install", "plouf"], expected=expected_lines)

    def test_trigger_exec_errors_out(self):
        """Make sure we print errors in triggered commands."""
        expected_lines = ["posttrans-triggers: /bin/ls: cannot access " \
                            "/path/to/inexistent/file: No such file or " \
                            "directory",
                          "posttrans-triggers: Failed to run command " \
                            "(/bin/ls /path/to/inexistent/file)"]
        self._run_yum_test(["install", "bidule"], expected=expected_lines)

    def test_exec_without_full_path(self):
        """Make sure commands are not executed without their full path."""
        expected_lines = ["posttrans-triggers: No such file or directory: " \
                           "echo"]
        unexpected_lines = ["Got trigger on path /usr/share/ouhlala (file is" \
                             "/usr/share/ouhlala/some_resource)"]

        self._run_yum_test(["install", "ouhlala"], expected=expected_lines,
                           unexpected=unexpected_lines)
