from ppl import EnableProroguedCallsStatic, PPLTypeError


class Example(metaclass=EnableProroguedCallsStatic):
    attribute = 42

    def foo(self):
        print("foo")


t = Example()
t.foo()  # Access already coded method

t.prorogued_method1(42, arg1=10)  # TYPING: ok (first call)
t.prorogued_method1(42, arg1=10)  # TYPING: ok, uses cached value
t.prorogued_method1(42, arg1=1)  # TYPING: ok, different argument

try:
    t.prorogued_method1(42)
except PPLTypeError as ex:
    print(repr(ex))  # PPLTypeError('prorogued_method1() missing 1 arguments')

try:
    t.prorogued_method1(42, arg=1)
except PPLTypeError as ex:
    # PPLTypeError('prorogued_method1() missing 1 required positional argument: arg1')
    print(repr(ex))

# WARNING: PPLSubTypeWarning(
# FunctionCallSignature: [<class 'int'>, arg1: <class 'int'>],
# FunctionCallSignature: [<class 'int'>, arg1: <class 'bool'>])
t.prorogued_method1(42, arg1=True)


res = t.prorogued_method1(42, arg1=10)  # TYPING: ok. Uses cached value

# When res is str, raise error. Otherwise continues execution. This is the normal Python behaviour
print(res + 3)
res.invalid_property  # raised always a error
