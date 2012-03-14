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
        # Check that both exec commands are executed
        expected_lines = ["posttrans-triggers: First trigger on " \
                           "/usr/share/machin",
                          "posttrans-triggers: Second trigger on " \
                           "/usr/share/machin"]
        output = self._run_yum_test(["install", "machin"],
                                    expected_lines)

        # Check the order in which they are executed
        def test_ordered_presence(lst1, lst2):
            """All elements in lst1 are also in lst2, in the same order."""
            start = 0
            try:
                for item in lst1:
                    start = lst2.index(item, start) + 1
            except ValueError:
                return False
            return True
        self.assertTrue(test_ordered_presence(expected_lines, output))

    def test_multiple_triggers_same_exec(self):
        """Make sure we run a given trigger command only once."""
        expected_lines = ["posttrans-triggers: /bin/systemctl reload " \
                           "trucmuche.service"]
        output = self._run_yum_test(["install", "trucmuche", "mod_trucmuche"],
                                    expected_lines)

        for line in expected_lines:
            self.assertEqual(output.count(line), 1)

    def test_multiple_triggers_multiple_similar_exec(self):
        """Make sure we run all exec commands for a given path, but only once."""
        # Check that both exec commands are executed
        expected_lines = ["posttrans-triggers: First trigger on " \
                           "/usr/share/machin",
                          "posttrans-triggers: Second trigger on " \
                           "/usr/share/machin"]
        output = self._run_yum_test(["install", "machin", "machins"],
                                    expected_lines)

        for line in expected_lines:
            self.assertEqual(output.count(line), 1)

    def test_multiple_triggers_similar_exec(self):
        """Make sure we try hard to run a given trigger command only once."""
        expected_lines = ["posttrans-triggers: /bin/systemctl reload " \
                           "trucmuche.service"]
        output = self._run_yum_test(["install", "trucmuche",
                                     "trucmuche-addons"],
                                    expected_lines)

        for line in expected_lines:
            self.assertEqual(output.count(line), 1)
