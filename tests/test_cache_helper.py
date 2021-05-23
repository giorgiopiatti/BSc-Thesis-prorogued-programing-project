import unittest
from ppl.cache_helper import freeze


class TestCacheHelper(unittest.TestCase):

    def test_freeze_does_not_fail_lists(self):
        a = [1, 2]
        freeze(a)
        a = [1, [1, 2, [1, 1]]]
        freeze(a)

    def test_freeze_does_not_fail_dicts(self):
        a = {'k0': 40, 'k1': 42}
        freeze(a)
        a = {'k0': 40, 'k1': [42, 42]}
        freeze(a)


if __name__ == '__main__':
    unittest.main()
