import unittest

from pyutttils.Member import Member


class TestMember(unittest.TestCase):
    def test_laruelli(self):
        self.assertEqual(Member(utt_login="laruelli").full_name, "Ivann LARUELLE")


if __name__ == '__main__':
    unittest.main()
