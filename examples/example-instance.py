from ppl import prorogue


class ExampleStatic(metaclass=prorogue.EnableProroguedCallsStatic):
    pass


print('\n----------EnableProroguedCallsStatic----------\n')
o1 = ExampleStatic()
o1.foo(42)


o2 = ExampleStatic()
o2.attribute = 4000
o2.foo(42)  # No interaction


print('\n----------EnableProroguedCallsInstance----------\n')


class ExampleInstance(metaclass=prorogue.EnableProroguedCallsInstance):
    pass


o1 = ExampleInstance()
o1.foo(42)

o1.foo(42)

o2 = ExampleInstance()
o2.foo(42)  # Interaction
o2.attribute = 1000
o2.foo(42)  # Interaction
