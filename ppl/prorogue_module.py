import sys
from types import ModuleType
from ppl.prorogue_handler import ProrogueHandler

import logging
logger = logging.getLogger(__name__)


class ModuleWrapper(ModuleType):

    def __metamodule_init__(self):
        # setattr(self, 'ModuleWrapper#original_module_name',
        #         name)  # prevent exposing this
        pass

    def __getattr__(self, name):
        original_module_name = self.__name__

        logger.info(f"{original_module_name}.{name} was referenced")

        def wrapper(*args, **kwargs):

            if type(args) is not tuple:
                args = (args, )

            pretty_args = args + \
                tuple([f'{k}={v}' for k, v in kwargs.items()])
            logger.info(
                f"{original_module_name}.{name} {pretty_args} was called")  # FIXME: format of kwargs

            handler = ProrogueHandler(self, name, args, kwargs)

            # Register a new function on the class
            setattr(self, name, handler.prorogued_fn)

            # Unpack parameters
            return handler.prorogued_fn(*args, **kwargs)
        return wrapper


def enable_module_level_prorogued_calls(name):
    """
        import ppl
        ppl.enable_module_level_prorogued_calls(__name__)
    """

    original_module = sys.modules[name]
    if isinstance(original_module, ModuleWrapper):  # Prevent wrong usage
        return

    original_module.__class__ = ModuleWrapper
    new_module = original_module

    # getattr(type(new_module), "__metamodule_init__", lambda self: None)(
    #     new_module)
    sys.modules[name] = new_module
