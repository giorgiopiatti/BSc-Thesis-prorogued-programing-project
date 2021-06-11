from ppl import PPLEnableProroguedCallsStatic, PPLTypeError


class Example(metaclass=PPLEnableProroguedCallsStatic):
    attribute = 42

    def foo(self):
        self.attribute_2 = 42*2
        print("foo")


t = Example()
t.foo()

res = t.prorogued_method1(42, arg1=10)  # TYPING: ok
print(f'RES: {res}, {type(res)}')

res = t.prorogued_method1(42, arg1=11)  # TYPING: ok
print(f'RES: {res}, {type(res)}')
