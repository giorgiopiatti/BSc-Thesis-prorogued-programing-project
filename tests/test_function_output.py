import unittest
from ppl.function_output import parse_to_python, TreeToPython


class TestFunctionOutput(unittest.TestCase):

    def compare_list(self, list):
        for test in list:
            self.compare(test)

    def compare(self, test):
        program_input = f'{test}'
        res = parse_to_python(program_input)
        self.assertEqual(res, test)

    def test_basic_types(self):
        basic_type = [1, 1.0, None, False, True]
        self.compare_list(basic_type)

    def test_string(self):
        self.assertEqual(parse_to_python('""'), "")
        self.assertEqual(parse_to_python('"Hello"'), "Hello")
        self.assertEqual(parse_to_python("'Hello'"), 'Hello')

    def test_tuple(self):
        tuples = [(1, 2, 3), (1, 1, 1)]
        self.compare_list(tuples)

    def test_tuple_singleton(self):
        self.compare((1,))

    def test_list(self):
        lists = [[1], [1, 2, 3], [1, 1, 1]]
        self.compare_list(lists)

    def test_dict(self):
        dicts = [{'a': 1, 'b': '2'}, {'a': 1}, {}]
        self.compare_list(dicts)

    def test_set(self):
        sets = [{'a', 'b', '2'}, {'a', 1}, {}]
        self.compare_list(sets)

    def test_free_var(self):
        expr = 'x'
        obj = TreeToPython.FreeVariable('x')
        self.assertEqual(parse_to_python(expr), obj)

        expr = '[x,x]'
        obj = TreeToPython.FreeVariable('x')
        self.assertEqual(parse_to_python(expr), [obj, obj])

    def test_free_var_context(self):
        def local_var(name):
            if name == 'x':
                return 42
            return None
        fn_context = {}
        fn_context['local_var'] = local_var

        res = parse_to_python('x', function_context=fn_context)
        self.assertEqual(res, 42)

    def test_complex_1(self):
        def local_var(name):
            if name == 'x':
                return 42
            if name == 'y':
                return 'Hello'
            if name == 'd':
                return {'a': 7}
            return None
        expr = '(x, y, {"key": d})'

        fn_context = {}
        fn_context['local_var'] = local_var
        res = parse_to_python(expr, function_context=fn_context)
        self.assertEqual(res, (42, 'Hello', {'key': {'a': 7}}))


if __name__ == '__main__':
    unittest.main()
