import unittest
from ppl.prorogue_handler import ProrogueHandler, PPLIncomparableTypeWarning, PPLSubTypeWarning, PPLSuperTypeWarning, PPLTypeError, PPLTypeWarning


class TestProroguedhandler(unittest.TestCase):

    def test_type_check_same_fn(self):

        p = ProrogueHandler('test_class', 'test',
                            (1, 4), {'k1': 's', 'k2': 42})

        self.assertTrue(
            p.fn_typecheck((1, 4), {'k1': 's', 'k2': 42}))

    def test_type_check_sub_type_warning(self):

        p = ProrogueHandler('test_class', 'test',
                            (1, 4), {'k1': 's', 'k2': 42})

        with self.assertRaises(PPLSubTypeWarning, msg='should detect bool <: int for positional arg'):
            p.fn_typecheck((1, True), {'k1': 's', 'k2': 42})

        with self.assertRaises(PPLSubTypeWarning, msg='should detect bool <: int for named arg'):
            p.fn_typecheck((1, 4), {'k1': 's', 'k2': True})

    def test_type_check_super_type_warning(self):

        p = ProrogueHandler('test_class', 'test',
                            (1, True), {'k1': 's', 'k2': 42})

        with self.assertRaises(PPLSuperTypeWarning, msg='should detect int :> bool positional arg'):
            p.fn_typecheck((1, 4), {'k1': 's', 'k2': 42})

        p = ProrogueHandler('test_class', 'test',
                            (1, 4), {'k1': 's', 'k2': True})

        with self.assertRaises(PPLSuperTypeWarning, msg='should detect int :> bool for named arg'):
            p.fn_typecheck((1, 4), {'k1': 's', 'k2': 42})

    def test_type_check_incomparable_warning(self):

        p = ProrogueHandler('test_class', 'test',
                            (1, True), {'k1': 's', 'k2': 42})

        with self.assertRaises(PPLIncomparableTypeWarning, msg='should return incomparable, not subtyping relation between the 2 signatures'):
            p.fn_typecheck((1, 's'), {'k1': 's', 'k2': 42})

        with self.assertRaises(PPLIncomparableTypeWarning, msg='should return incomparable, not subtyping relation between the 2 signatures'):
            p.fn_typecheck((1, {}), {'k1': 's', 'k2': 42})

    def test_type_check_missing_parameters(self):
        p = ProrogueHandler('test_class', 'test',
                            (1, True), {'k1': 's', 'k2': 42})

        with self.assertRaises(PPLTypeError, msg='should detect missing positional parameter'):
            p.fn_typecheck((1,), {'k1': 's', 'k2': 42})

        with self.assertRaises(PPLTypeError, msg='should detect additional positional parameter'):
            p.fn_typecheck((1, True, 3), {'k1': 's', 'k2': 42})

        with self.assertRaises(PPLTypeError, msg='should detect missing named parameter'):
            p.fn_typecheck((1, True), {'k1': 's'})

        with self.assertRaises(PPLTypeError, msg='should detect missing named parameter'):
            p.fn_typecheck((1, True), {'k2': 's'})

        with self.assertRaises(PPLTypeError, msg='should detect wrong named parameter'):
            p.fn_typecheck((1, True), {'k1': 's', 'k': 42})

        with self.assertRaises(PPLTypeError, msg='should detect additional named parameter'):
            p.fn_typecheck((1, True), {'k1': 's', 'k2': 42, 'k3': ''})


if __name__ == '__main__':
    unittest.main()
