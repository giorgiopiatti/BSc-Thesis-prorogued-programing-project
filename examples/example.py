from ppl import prorogue


class Example(metaclass=prorogue.EnableProroguedCallsStatic):

    def foo(self):
        print("foo")

    def bar(self):
        print("bar")
        o = self.prorogued_method2("Hi")
        print(o)


t = Example()
t.foo()
t.bar()
t.bar()
t.prorogued_method2("Input1")
t.prorogued_method2("Input1")

print('----------First call to prorogued_method1----------')
t.prorogued_method1(42, test=10)

print('----------Second call to prorogued_method1----------')
t.prorogued_method1(42, test=10)

print('----------Third call to prorogued_method1 with TypeError----------')
t.prorogued_method1(43, 23, 10)
