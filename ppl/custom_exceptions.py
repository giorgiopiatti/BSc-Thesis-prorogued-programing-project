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
