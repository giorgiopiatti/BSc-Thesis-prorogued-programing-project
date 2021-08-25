import logging
from ppl.prorogue_handler import ProrogueHandler
from ppl import config

logger = logging.getLogger(__name__)


class PPLEnableProroguedCallsStatic(type):
    '''
        Metaclass to allow prorogued methods inside a class.
        Handles the injection of code via Python built-in methods

        Static methods: i.e. prorogued functions is bound by class and not instance

    '''

    def __new__(metacls, name, bases, namespace, **kwargs):
        return super().__new__(metacls, name, bases, namespace)

    def __init__(cls, object_or_name, bases, dict, **kwargs):
        super().__init__(object_or_name, bases, dict)

        do_cache = True
        if 'cache' in kwargs.keys() and kwargs['cache'] is False:
            do_cache = False

        def getattr(self, name):
            if config.get_status():
                raise AttributeError(
                    f"'{self.__class__.__name__}' has no attribute '{name}'")

            logger.info(f"{self.__class__}.{name} was referenced")

            def wrapper(*args, **kwargs):

                if type(args) is not tuple:
                    args = (args, )

                pretty_args = args + \
                    tuple([f'{k}={v}' for k, v in kwargs.items()])
                logger.info(
                    f"{self.__class__}.{name} {pretty_args} was called")  # FIXME: format of kwargs

                handler = ProrogueHandler(
                    self, name, args, kwargs, do_cache=do_cache)

                # Register a new function on the class
                setattr(cls, name, handler.prorogued_fn)

                # Unpack parameters
                return handler.prorogued_fn(*args, **kwargs)
            return wrapper
        cls.__getattr__ = getattr


class PPLEnableProroguedCallsInstance(type):
    '''
        Metaclass to allow prorogued methods inside a class.
        Handles the injection of code via Python built-in methods

        Prorogued function is bounded by object instance not by class
    '''

    def __new__(metacls, name, bases, namespace, **kwargs):
        return super().__new__(metacls, name, bases, namespace)

    def __init__(cls, object_or_name, bases, dict, **kwargs):
        super().__init__(object_or_name, bases, dict)

        do_cache = True
        if 'cache' in kwargs.keys() and kwargs['cache'] is False:
            do_cache = False

        def getattr(self, name):
            if config.get_status():
                raise AttributeError(
                    f"'{self.__class__.__name__}' has no attribute '{name}'")

            logger.info(f"{self.__class__}.{name} was referenced")

            def wrapper(*args, **kwargs):
                pretty_args = args + \
                    tuple([f'{k}={v}' for k, v in kwargs.items()])
                logger.info(
                    f"{self.__class__}.{name} {pretty_args} was called")  # FIXME: format of kwargs

                handler = ProrogueHandler(
                    self, name, args, kwargs, instance_call=True, do_cache=do_cache)

                # Register a new function on the object, notice how the function is the same for the whole class. i.e. we capture the fact that the
                # function could depend from the object state
                setattr(self, name, handler.prorogued_fn)
                return handler.prorogued_fn(*args, **kwargs)

            return wrapper
        cls.__getattr__ = getattr


def prorogue(do_cache=True):
    def dec(function):
        def wrapper(*args, **kwargs):
            handler = ProrogueHandler(
                "", function.__name__, args, kwargs, do_cache=do_cache)
            return handler.prorogued_fn(*args, **kwargs)

        return wrapper
    return dec


def prorogue_method(do_cache=True):
    def dec(function):
        def wrapper(self, *args, **kwargs):
            handler = ProrogueHandler(
                self, function.__name__, args, kwargs, do_cache=do_cache)
            return handler.prorogued_fn(*args, **kwargs)

        return wrapper
    return dec
