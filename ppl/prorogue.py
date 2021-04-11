import logging
from ppl.prorogue_handler import ProrogueHandler

logger = logging.getLogger(__name__)


class EnableProroguedCallsStatic(type):
    '''
        Metaclass to allow prorogued methods inside a class.
        Handles the injection of code via Python built-in methods

        Static methods: i.e. prorogued functions is bound by class and not instance

    '''

    def __init__(cls, object_or_name, bases, dict):
        super().__init__(object_or_name, bases, dict)

        def getattr(self, name):
            logger.info(f"{self.__class__}.{name} was referenced")

            def wrapper(*args, **kwargs):

                if type(args) is not tuple:
                    args = (args, )

                pretty_args = args + \
                    tuple([f'{k}={v}' for k, v in kwargs.items()])
                logger.info(
                    f"{self.__class__}.{name} {pretty_args} was called")  # FIXME: format of kwargs

                handler = ProrogueHandler(self.__class__, name, args, kwargs)

                # Register a new function on the class
                setattr(cls, name, handler.prorogued_fn)

                return handler.prorogued_fn(*args, *kwargs) # Unpack parameters 
            return wrapper
        cls.__getattr__ = getattr


class EnableProroguedCallsInstance(type):
    '''
        Metaclass to allow prorogued methods inside a class.
        Handles the injection of code via Python built-in methods

        Prorogued function is bounded by object instance not by class
    '''

    def __init__(cls, object_or_name, bases, dict):
        super().__init__(object_or_name, bases, dict)

        def getattr(self, name):
            logger.info(f"{self.__class__}.{name} was referenced")

            def wrapper(*args, **kwargs):
                pretty_args = args + \
                    tuple([f'{k}={v}' for k, v in kwargs.items()])
                logger.info(
                    f"{self.__class__}.{name} {pretty_args} was called")  # FIXME: format of kwargs

                handler = ProrogueHandler(self.__class__, name, args, kwargs)

                # Register a new function on the object, notice how the function is the same for the whole class. i.e. we capture the fact that the
                # function could depend from the object state
                setattr(self, name, handler.prorogued_fn)

                return handler.prorogued_fn(*args, **kwargs)

            return wrapper
        cls.__getattr__ = getattr
