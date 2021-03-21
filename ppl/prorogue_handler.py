import logging
import sys
import functools

logger = logging.getLogger(__name__)


class ProrogueHandler:

    def __init__(self, class_name, name, args, kwargs):
        self.args_list = args
        self.args_dict = kwargs
        self.name = name
        self.class_name = class_name

    def fn_typecheck(self, args, kwargs):
        '''
            Perform the typecheck for the function. We refine the judgment from the first call to subsequent calls.

            Currently it performs only argument count checks and keyword matching.

            Since Python programming model allow to pass arguments in 2 ways: positional or named, we have a gray area:
            When calling the function with a named argument and not all positional arguments were provided it could be that the programmer assumed this
            was the name.
            TODO: develop a better strategy idea and describe this in the paper
            TODO: collect possible names and then check for subsequent calls

            TODO: implement subtyping checks
        '''
        logger.debug(
            f'fn_typecheck for {self.name} with arg_list={self.args_list}, args_dict={self.args_dict}, args={args}, kwargs={kwargs}')
        if len(args) > (len(self.args_list) + len(self.args_dict)):
            raise TypeError(
                f'{self.name}() takes {(len(self.args_list) + len(self.args_dict))} positional arguments but {len(args)} were given')

        if len(args) + len(kwargs) < (len(self.args_list) + len(self.args_dict)):
            raise TypeError(
                f'{self.name}() missing {len(self.args_list) + len(self.args_dict) - len(args) - len(kwargs)} arguments')

        number_positional_args_as_keyword = len(self.args_list) - len(args)
        candidate_positional_args = []

        for k in kwargs.keys():
            if k not in self.args_dict and number_positional_args_as_keyword == 0:
                raise TypeError(
                    f'{self.name}() got an unexpected keyword argument {k}')
            elif k not in self.args_dict:
                candidate_positional_args.append(k)
                number_positional_args_as_keyword -= 1

        # Exclude keyword parameters passed as positional, then check if all expected keywords are present
        for k in list(self.args_dict.keys())[(len(args) - len(self.args_list)):]:
            if k not in kwargs:
                raise TypeError(
                    f'{self.name}() missing 1 required positional argument: {k}')

        if len(candidate_positional_args) > 0:
            logger.warning(
                f"While typechecking {self.name}() discovered some positional args expressed with keywords that we cannot handle.")

    # Caches previous return's value by hash of all input parameters
    @functools.lru_cache(maxsize=None)
    def prorogued_fn(self, *args, **kwargs):
        logger.info(
            f"{self.class_name}.{self.name} ***************ProrogueHandler***************")

        try:
            self.fn_typecheck(args, kwargs)
        except TypeError as ex:  # Skip internal traceback, better preserves expected behavior to end programmer
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
