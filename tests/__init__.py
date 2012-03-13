import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


from .test_simple import *
from .test_errors import *
from .test_merging import *
