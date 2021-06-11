# Prorogued Programming Language - Prototype for Python

In this repository we have the library code in the folder `ppl`.
To run the code snippets found in the example folder, you need first to run the setup script `setup.sh`, which creates a Python virtual environment and install the dependencies.

Each time a new terminal is open: `source venv/bin/activate`


## Library documentation

The activation the prorogued programming paradigm behavior is done at class level, we leverage the usage of metaclasses. To active this for a given class A you need to use one of the two available metaclasses:
 - `prorogue.PPLEnableProroguedCallsStatic`: each prorogued call is bounded to the object class, this models the behavior of static methods
 - `prorogue.PPLEnableProroguedCallsInstance`: each prorogued call is bounded to the object instance, this models the behavior of instance methods. (The output of the prorogued method could depend on the internal object state, and this same input doesn't lead to same output)


 Run tests
 `python3 -m unittest tests` -v for verbose