from __future__ import annotations
from collections import OrderedDict


class FunctionCallSignature:
    '''
    This class describes the signature of a prorogued function call.

    It assumes that positional arguments and keyword arguments do not overlap.

    '''

    def __init__(self, args, kwargs):
        self.args = []
        self.kwargs = []

        counter_position = 0
        for a in args:
            self.args.append(FunctionArgument(
                type(a), position=counter_position))
            counter_position += 1
        # sorts by keword such that future comparisons are easier
        for k, v in kwargs.items():
            self.kwargs.append(FunctionArgument(
                type(v), name=k))

    def compare(self, op, value):
        res = True
        err_msg = []

        if len(self.args) != len(value.args):
            return False, []

        for x, y in zip(self.args, value.args):
            if not op(x, y):
                res = False
                err_msg.append(TypeMistmatch(x, y))

        if len(self.kwargs) != len(value.kwargs):
            return False, []

        for x, y in zip(self.kwargs, value.kwargs):
            if not op(x, y):
                res = False
                err_msg.append(TypeMistmatch(x, y))

        return res, err_msg

    def is_equal(self, value):
        return self.compare(FunctionArgument.__eq__, value)

    def __eq__(self, value):
        res, _ = self.compare(FunctionArgument.__eq__, value)
        return res

    def __le__(self, value):
        res, _ = self.compare(FunctionArgument.__le__, value)
        return res

    def __repr__(self):
        s = 'FunctionCallSignature: ['
        for fa in self.args:
            s += str(fa) + ',\n'
        for fa in self.kwargs:
            s += str(fa) + ',\n'
        s = s[:-2] + ']'
        return s

    def __str__(self):
        s = '('
        for fa in self.args:
            s += str(fa) + ', '
        for fa in self.kwargs:
            s += str(fa) + ', '
        s = s[:-2] + ')'
        return s

    def get_keywords(self):
        return list(map(lambda x: x.name, self.kwargs))

    def __hash__(self):
        return hash((*self.args, *self.kwargs))


class TypeMistmatch:

    def __init__(self, first, other):
        self.first = first
        self.other = other

    def __eq__(self, value):
        return self.first == value.first and self.other == value.other


class FunctionArgument:
    def __init__(self, t, name=None, position=None):
        self.type = t
        self.name = name
        self.position = position

    def __repr__(self):
        return f'(name={self.name}, pos={self.position}, type={self.type})'

    def __str__(self):
        if self.name is None:
            return f'{self.type}'
        else:
            return f'{self.name}: {self.type}'

    def __eq__(self, value: FunctionArgument):
        return self.type == value.type and self.is_equal_id(value)

    def __ne__(self, value: FunctionArgument):
        return not __eq__(self, value)

    def __le__(self, value: FunctionArgument):
        return self.__eq__(value) or self.__lt__(value)

    def __lt__(self, value: FunctionArgument):
        strictly_subtype = issubclass(
            self.type, value.type) and not issubclass(value.type, self.type)
        return strictly_subtype and self.is_equal_id(value)

    def is_equal_id(self, value: FunctionArgument):
        return self.name == value.name and self.position == value.position

    def __hash__(self):
        return hash((self.type, self.name, self.position))
