from ppl import prorogue, prorogue_method, PPLEnableProroguedCallsStatic


@prorogue()
def f(i):
    return i


f(43)


class Example(metaclass=PPLEnableProroguedCallsStatic):
    attribute = 42

    @prorogue_method()
    def foo(self):
        print("foo")


t = Example()
t.foo()  # Access already coded method
