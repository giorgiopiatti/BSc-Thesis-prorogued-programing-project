import logging
import sys
import functools

from ppl.function_signature import FunctionCallSignature
from ppl.custom_exceptions import PPLIncomparableTypeWarning, PPLSubTypeWarning, PPLSuperTypeWarning, PPLTypeError, PPLTypeWarning

from ppl.function_output import parse_to_python
from lark.exceptions import UnexpectedToken, VisitError

from ppl.cache_helper import cache_key

from ppl.io import write, get_input, write_instance, error_message
import cachetools

logger = logging.getLogger(__name__)


class ProrogueHandler:

    def __init__(self, instance, name, args, kwargs, instance_call=False, do_cache=True):
        self.name = name
        self.instance = instance
        self.class_name = instance.__class__.__name__
        self.first_call_signature = FunctionCallSignature(args, kwargs)
        if instance_call:
            self.ppl_instance_dict = instance.__dict__
        else:
            self.ppl_instance_dict = None
        self.instance_call = instance_call
        self.do_cache = do_cache

    def fn_typecheck(self, args: tuple, kwargs: dict):
        '''
            Perform the typecheck for the function. We refine the judgment from the first call to subsequent calls.

            Currently it performs only argument count checks and keyword matching.

            Since Python programming model allow to pass arguments in 2 ways: positional or named, we have a gray area:
            When calling the function with a named argument and not all positional arguments were provided it could be that the programmer assumed this
            was the name. This case is not handled, we assume that positional arguments are passed as positional, and the same for keyword arguments.
        '''
        if type(args) is not tuple:
            raise AttributeError('args must be a tuple')
        if type(kwargs) is not dict:
            raise AttributeError('kwards must be a dictionary')

        logger.debug(
            f'fn_typecheck for {self.name} with arg_list={self.first_call_signature.args}, kwargs={self.first_call_signature.kwargs}, args={args}, kwargs={kwargs}')

        call_fn_sig = FunctionCallSignature(args, kwargs)

        # Number of arguments doesn't match
        if len(args) + len(kwargs) < (len(self.first_call_signature.args) + len(self.first_call_signature.kwargs)):
            raise PPLTypeError(
                f'{self.name}() missing {len(self.first_call_signature.args) + len(self.first_call_signature.kwargs) - len(args) - len(kwargs)} arguments')

        if len(args) + len(kwargs) > (len(self.first_call_signature.args) + len(self.first_call_signature.kwargs)):
            raise PPLTypeError(
                f'{self.name}() got additional {len(self.first_call_signature.args) + len(self.first_call_signature.kwargs) - len(args) - len(kwargs)} arguments, expecting {len(self.first_call_signature.args) + len(self.first_call_signature.kwargs)}')

        if len(args) != len(self.first_call_signature.args):
            raise PPLTypeError(
                f'{self.name}() expected {len(self.first_call_signature.args)} but got {len(args)} positional arguments'
            )

        if len(kwargs) != len(self.first_call_signature.kwargs):
            raise PPLTypeError(
                f'{self.name}() expected {len(self.first_call_signature.kwargs)} but got {len(kwargs)} keyword arguments'
            )

        # Assumption: same number of positional and keyword arguments
        is_same_sig, msg = self.first_call_signature.is_equal(call_fn_sig)

        if not is_same_sig:
            if call_fn_sig <= self.first_call_signature:
                # Between the first call and this call there is a subtyping relationship
                # In this case we should continue execution and output a warning
                raise PPLSubTypeWarning(
                    self.first_call_signature, call_fn_sig)
            elif self.first_call_signature <= call_fn_sig:
                raise PPLSuperTypeWarning(
                    self.first_call_signature, call_fn_sig)
            else:
                # Check that that all keyword arguments are the same:
                # - all required keywords are present in `call_fn_sig`
                # - no additional keyword is present in `call_fn_sig`
                keys0 = self.first_call_signature.get_keywords()
                keys1 = call_fn_sig.get_keywords()
                for k in keys0:
                    if k not in keys1:
                        raise PPLTypeError(
                            f'{self.name}() missing 1 required positional argument: {k}')
                for k in keys1:
                    if k not in keys0:
                        raise PPLTypeError(
                            f'{self.name}() got an unexpected keyword argument {k}')

                # Length and keywords matches, but typing information is incomparable.
                #
                # Note this could be that the desidered function type is the join of both types (or an ancestor of the join of these 2 types)
                raise PPLIncomparableTypeWarning(
                    self.first_call_signature, call_fn_sig)

        return True

    # We need to be able to pass all possible parameters, this is the most possible general function in Python
    def prorogued_fn(self, *args, **kwargs):
        logger.info(
            f"{self.class_name}.{self.name} running ProrogueHandler")
        signature = FunctionCallSignature(args, kwargs)
        while True:
            try:
                self.fn_typecheck(args, kwargs)
                out = self.wrapper_get_out(
                    signature, *args, ppl_instance_dict=self.ppl_instance_dict, **kwargs)
                return out
            # Skip internal traceback, better preserves expected behavior to end programmer TODO: skip also this layer, but how?
            except (PPLTypeError) as ex:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                try:
                    exc_traceback = exc_traceback.tb_next
                    exc_traceback = exc_traceback.tb_next
                except Exception:
                    pass
                error_message(f'Error: {repr(ex)}')
                #raise ex.with_traceback(exc_traceback)
            except PPLTypeWarning as ex:
                write(f'WARNING: {repr(ex)}')
                out = self.wrapper_get_out(
                    signature, *args, ppl_instance_dict=self.ppl_instance_dict,  **kwargs)
                return out

    # Caches previous return's value by hash of all input parameters
    @cachetools.cached(cache={}, key=cache_key)
    def wrapper_get_out_cache(self, signature, *args, ppl_instance_dict, **kwargs):
        out = self.ask_for_output(args, kwargs)
        return out

    def wrapper_get_out(self, signature, *args, ppl_instance_dict, **kwargs):
        if self.do_cache:
            return self.wrapper_get_out_cache(signature, *args, ppl_instance_dict=ppl_instance_dict, **kwargs)
        else:
            return  self.ask_for_output(args, kwargs)

    def save_return_value(self, programmer_input, kwargs):
        # We create different function context
        # one for the variables in scope only of the function, and an other for
        # variables that can be accessed via 'self', and for class variables
        function_context = {}

        def local_var(name):
            if name in kwargs:
                return kwargs[name]
            raise PPLTypeError(f'{name} not found in scope')

        def instance_var(name):
            if name in self.instance.__dict__:
                return self.instance.__dict__[name]
            raise PPLTypeError(f'{name} not found in scope')

        def class_var(base, name):
            if base == self.instance.__class__.__name__ and \
                    name in self.instance.__class__.__dict__:
                return self.instance.__class__.__dict__[name]
            raise PPLTypeError(f'{name} not found in scope')

        function_context['local_var'] = local_var
        function_context['instance_var'] = instance_var
        function_context['class_var'] = class_var

        return parse_to_python(programmer_input, function_context=function_context)

    def ask_for_output(self, args, kwargs):

        pretty_print = ""
        if len(args) == 1:
            pretty_print += str(args)[1:-2]
        elif len(args) > 1:
            pretty_print += str(args)[1:-1]

        if len(kwargs) > 0:
            pretty_print += ", "
            for (k, v) in kwargs.items():
                pretty_print += f"{k}={v}, "
            pretty_print = pretty_print[:-2]

        write(
            f'> Function call to {self.class_name}.{self.name}({pretty_print}) was prorogued.')
        # TODO: we need to expose which object is associated, and its internal structure if we're using PPLEnableProroguedCallsInstance

        if self.instance_call:
            write_instance(
                f'{self.class_name} instance dict: {self.ppl_instance_dict}')
        else:
            write_instance('')

        # Ask the programmer for value (only built-in type supported until now)
        while True:
            value = get_input('Insert prorogued call return value: ')
            res = None
            try:
                res = self.save_return_value(value, kwargs)
                break
            except UnexpectedToken:
                write('> Invalid expression!')
            except VisitError as e:
                raise e.orig_exc from None

        return res
