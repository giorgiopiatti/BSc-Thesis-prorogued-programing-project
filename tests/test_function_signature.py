import unittest
from ppl.function_signature import FunctionCallSignature, FunctionArgument, TypeMistmatch


class TestFunctionSignature(unittest.TestCase):

    def test_eq(self):
        fn_sig = FunctionCallSignature((1, 2, 3), {'k1': '', 'k2': 42})
        self.assertTrue(fn_sig == fn_sig)

        fn_sig1 = FunctionCallSignature((1, 2, 3), {'k1': '', 'k2': 42})
        fn_sig2 = FunctionCallSignature((1, 2), {'k1': '', 'k2': 42})

        self.assertFalse(fn_sig1 == fn_sig2)

    def test_compare_eq(self):

        fn_sig1 = FunctionCallSignature((1, 2, 3), {'k1': '', 'k2': 42})
        fn_sig2 = FunctionCallSignature((1, 2), {'k1': '', 'k2': 42})

        res, msg = fn_sig1.compare(FunctionArgument.__eq__, fn_sig2)
        self.assertFalse(res)
        self.assertTrue(len(msg) == 0)

        fn_sig1 = FunctionCallSignature((1, 2, 3), {'k1': '', 'k2': 42})
        fn_sig2 = FunctionCallSignature((1, 2, 's'), {'k1': '', 'k2': 42})

        res, msg = fn_sig1.compare(FunctionArgument.__eq__, fn_sig2)
        self.assertFalse(res)
        self.assertTrue(len(msg) == 1)
        self.assertTrue(msg[0] == TypeMistmatch(
            FunctionArgument(int, position=2), FunctionArgument(str, position=2)))


if __name__ == '__main__':
    unittest.main()
