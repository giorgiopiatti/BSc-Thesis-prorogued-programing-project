from ppl import prorogue


class ExampleStatic(metaclass=prorogue.PPLEnableProroguedCallsStatic):
    pass


print('\n----------PPLEnableProroguedCallsStatic----------\n')
o1 = ExampleStatic()
o1.foo(42)


o2 = ExampleStatic()
o2.attribute = 4000
o2.foo(42)  # No interaction


print('\n----------PPLEnableProroguedCallsInstance----------\n')


class ExampleInstance(metaclass=prorogue.PPLEnableProroguedCallsInstance):
    pass


o1 = ExampleInstance()
o1.foo(42)

o1.foo(42)

o2 = ExampleInstance()
o2.foo(42)  # Interaction
o2.attribute = 1000
o2.foo(42)  # Interaction
