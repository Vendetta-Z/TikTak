from unittest import TestCase
# Create your tests here.


def index(a):
    return a+a


class TestTiktak(TestCase):
    def test_index(self):
        self.assertEqual(index(1), 2)
