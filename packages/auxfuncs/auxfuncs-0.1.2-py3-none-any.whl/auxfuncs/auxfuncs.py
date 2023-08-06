from collections.abc import Sequence, Callable
from inspect import signature
from multimethod import multimethod

@multimethod
def _reduce_args(func: Callable, args: Sequence=None, arg_index: int=None) -> Callable:
    if len(signature(func).parameters) == 1: #If function has only one parameter, return function itself.
        return func
    else:
        raise TypeError(f'If function has more than one parameter, then args and arg_index must be defined as Sequence and int respectively. args: {args}, arg_index: {arg_index}')

@multimethod
def _reduce_args(func: Callable, args: Sequence, arg_index: int) -> Callable:
    def reduced_func(x):
        args[arg_index] = x
        return func(*args)
    return reduced_func

def reduce_args(func: Callable, args: Sequence=None, arg_index: int=None) -> Callable:
    '''
    Returns a function that has been reduced to a single argument.
    ----------        
    Parameters:
    ----
        func (Callable): Python function to be reduced.
        args (Sequence): Optional. Sequence of arguments to be passed to the function. Example: func(x, y) -> z, args = [x, y]. Not needed if function has only one parameter (default None)
        arg_index (int): Optional. Index of the argument to be passed to the function. Example: func(x, y) -> z, arg_index = 1. Not needed if function has only one parameter (default None)
    ----
    Returns:
    ----
        reduced_func (Callable): A function that has been reduced to a single argument.
    '''
    try:
        reduced_func = _reduce_args(func, args, arg_index)
        return reduced_func
    except TypeError as e:
        raise e