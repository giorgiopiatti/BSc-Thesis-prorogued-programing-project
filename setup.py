from setuptools import find_packages, setup
setup(
    name='ppl',
    packages=['ppl'],
    version='0.0.1',
    description='',
    author='Giorgio Piatti',
    license='',
    install_requires=['lark-parser==0.11.2', 'cachetools==4.2.2', 'tk==0.1.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
