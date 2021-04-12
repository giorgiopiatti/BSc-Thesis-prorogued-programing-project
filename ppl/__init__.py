import logging

from ppl.prorogue import EnableProroguedCallsStatic, EnableProroguedCallsInstance
from ppl.custom_exceptions import PPLIncomparableTypeWarning, PPLSubTypeWarning, PPLSuperTypeWarning, PPLTypeError, PPLTypeWarning

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s', level=logging.DEBUG)
