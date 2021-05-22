from lark import Lark, Transformer, v_args
import logging

logger = logging.getLogger(__name__)

# TODO: implement access to free variables via self keyword

return_value_grammar = r"""
    expression: tuple
                 | list
                 | dict
                 | set
                 | singleton
                 | atom

    ?atom: SIGNED_FLOAT -> float
        | SIGNED_INT -> int
        | "True" -> true
        | "False" -> false
        | "None" -> none
        | STRING_ESCAPED_QUOTES -> string
        | id -> local_var
        | instance_var
        | class_var

    id: CNAME -> identifier

    instance_var: "self." id
    class_var: id "." id

    kvpair: atom ":" expression
    singleton: "(" expression "," ")"
    tuple:  "(" [expression ("," expression)*]")"
    list: "[" [expression ("," expression)*] "]"
    dict: "{" [kvpair ("," kvpair)*] "}"
    set: "{" [expression ("," expression)*]  "}"

    STRING_ESCAPED_QUOTES: /[\"'][^\"']*[\"']/

    %import common.CNAME
    %import common.SIGNED_FLOAT
    %import common.SIGNED_INT
    %import common.WS

    %ignore WS
    """


class TreeToPython(Transformer):

    def __init__(self, function_context=None, *args, **kwargs):
        self.function_context = function_context
        super().__init__(*args, **kwargs)

    def none(self, _): return None
    def true(self, _): return True
    def false(self, _): return False

    float = v_args(inline=True)(float)
    int = v_args(inline=True)(int)
    kvpair = tuple

    def expression(self, args):
        return args[0]

    def elem(self, args):
        return args

    def tuple(self, args):
        return tuple(args)

    def singleton(self, arg):
        return (arg[0], )

    def list(self, args):
        return list(args)

    def dict(self, args):
        return dict(args)

    def set(self, args):
        return set(args)

    def str_remove_quotes(self, x):
        x = str(x)
        return x[1:-1]
    string = v_args(inline=True)(str_remove_quotes)

    class FreeVariable():
        def __init__(self, name):
            self.name = name

        def __repr__(self):  # This should support arguments of proprogued function and also variable available in the scope
            return f'FreeVar({self.name})'

        def __eq__(self, value):
            return self.name == value.name

    def local_var(self, name):
        if self.function_context is None:
            return self.FreeVariable(name)
        else:
            return self.function_context['local_var'](name)

    def instance_var(self, name):
        if self.function_context is None:
            return self.FreeVariable(name)
        else:
            return self.function_context['instance_var'](name)

    def class_var(self, base, name):
        if self.function_context is None:
            return self.FreeVariable(name)
        else:
            return self.function_context['class_var'](base, name)

    identifier = v_args(inline=True)(str)
    local_var = v_args(inline=True)(local_var)
    instance_var = v_args(inline=True)(instance_var)
    class_var = v_args(inline=True)(class_var)


def parse_to_python(programmer_input, function_context=None):
    parser = Lark(return_value_grammar, start='expression',
                  parser='earley', debug=True)
    ast = parser.parse(programmer_input)
    logger.debug(f'AST of "{programmer_input}" is {ast}')
    res = TreeToPython(function_context=function_context,
                       visit_tokens=True).transform(ast)
    logger.debug(f'AST to Python: {res}')
    return res
