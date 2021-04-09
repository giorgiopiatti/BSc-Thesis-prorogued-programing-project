import logging
import sys
import functools

from ppl.function_signature import FunctionCallSignature

logger = logging.getLogger(__name__)


# START - define custom exceptions

class PPLTypeError(TypeError):
    '''
   TypeError: This error is raised when we are sure that typing does not succeeded 
    '''
    pass


class PPLTypeWarning(Exception):
    '''
    General TypeWarning. First parameter is the first seen prorogued calls, the second parameter is instead the 
    signature, within this warning was raised.
    '''

    def __init__(self, first_call_signature, call_signature):
        self.first_call_signature = first_call_signature
        self.call_signature = call_signature


class PPLSubTypeWarning(PPLTypeWarning):
    '''
        call_signature <: first_call_signature 
    '''
    pass


class PPLSuperTypeWarning(PPLTypeWarning):
    '''
        call_signature :> first_call_signature 
    '''
    pass


class PPLIncomparableTypeWarning(PPLTypeWarning):
    '''
        Both statements call_signature :> first_call_signature and  call_signature <: first_call_signature  do not hold.
    '''
    pass

# END - define custom exceptions


class ProrogueHandler:

    def __init__(self, class_name, name, args, kwargs):
        self.name = name
        self.class_name = class_name
        self.first_call_signature = FunctionCallSignature(args, kwargs)

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

    # Caches previous return's value by hash of all input parameters
    @functools.lru_cache(maxsize=None)
    def prorogued_fn(self, args, kwargs):
        logger.info(
            f"{self.class_name}.{self.name} ***************ProrogueHandler***************")

        try:
            self.fn_typecheck(args, kwargs)
        # Skip internal traceback, better preserves expected behavior to end programmer TODO: skip also this layer, but how?
        except (PPLTypeError, PPLTypeWarning) as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            try:
                exc_traceback = exc_traceback.tb_next
                exc_traceback = exc_traceback.tb_next
            except Exception:
                pass
            ex.__traceback__ = exc_traceback
            raise ex

        out = input(
            f'Function call to {self.name}({args},{kwargs}) was prorogued, please enter the expected output: ')
        # TODO: we need to expose which object is associated, and its internal structure if we're using EnableProroguedCallsInstance
        return out
