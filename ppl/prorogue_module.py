import sys
from types import ModuleType
from ppl.prorogue_handler import ProrogueHandler
from ppl import config

import logging
logger = logging.getLogger(__name__)


class ModuleWrapper(ModuleType):

    def __metamodule_init__(self):
        pass

    def __getattr__(self, name):
        if config.get_status():
            raise AttributeError(
                f"module '{__name__}' has no attribute '{name}'")

        original_module_name = self.__name__

        logger.info(f"{original_module_name}.{name} was referenced")

        def wrapper(*args, **kwargs):

            if type(args) is not tuple:
                args = (args, )

            pretty_args = args + \
                tuple([f'{k}={v}' for k, v in kwargs.items()])
            logger.info(
                f"{original_module_name}.{name} {pretty_args} was called")

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
    new_module.__class__.__name__ = name

    sys.modules[name] = new_module
