import logging

from ppl.prorogue import EnableProroguedCallsStatic, EnableProroguedCallsInstance
from ppl.custom_exceptions import PPLIncomparableTypeWarning, PPLSubTypeWarning, PPLSuperTypeWarning, PPLTypeError, PPLTypeWarning

from ppl.prorogue_module import enable_module_level_prorogued_calls
import ppl.config


logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s', level=logging.DEBUG, filename='./ppl.log')
