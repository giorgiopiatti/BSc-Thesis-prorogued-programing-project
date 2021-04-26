from ppl import EnableProroguedCallsStatic, PPLTypeError


class Example(metaclass=EnableProroguedCallsStatic):
    attribute = 42

    def foo(self):
        self.test = 69
        print("foo")


t = Example()
t.foo()

res = t.prorogued_method1(42, arg1=10)  # TYPING: ok
print(f'RES: {res}, {type(res)}')

res = t.prorogued_method1(42, arg1=11)  # TYPING: ok
print(f'RES: {res}, {type(res)}')
