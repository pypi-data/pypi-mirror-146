# pip install line_profiler
from line_profiler import LineProfiler
from functools import wraps
import numpy as ny
import torch

DEBUG_TIME_ANALYSIS = True

#查询接口中每行代码执行的时间
def func_line_time(f):
    if DEBUG_TIME_ANALYSIS:
        @wraps(f)
        def decorator(*args, **kwargs):
            func_return = f(*args, **kwargs)
            lp = LineProfiler()
            lp_wrap = lp(f)
            lp_wrap(*args, **kwargs) 
            lp.print_stats() 
            return func_return 
        return decorator
    else:
        def I(*args, **kwargs):
            return f(*args, **kwargs)
        return I

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(counter = 0)
def filterWriter(s):
    if 'SOURCE IS UNAVAILABLE' in s:
        filterWriter.counter = s.split()[1]
        pass
    else:
        print("Line {}: {}".format(filterWriter.counter, s[:-1]))
        
def print_list_size(l):
    # return 'list(size={})'.format(len(l))
    return ''
    
def print_ndarray(a):
    return 'ndarray(shape={}, dtype={})'.format(a.shape, a.dtype)

def print_tensor(a):
    return 'tensor(shape={}, dtype={}, device={})'.format(a.shape, a.dtype, a.device)

def var_printer(func):
    @wraps(func)
    def wrapper(*arg, **kw):
        func_return = func(*arg, **kw)
        pysnoo = pysnooper.snoop(output=filterWriter, prefix='', custom_repr=((list, print_list_size), (np.ndarray, print_ndarray), (torch.Tensor, print_tensor)), normalize=True)
        pysnooper_wrap = pysnoo(func)
        pysnooper_wrap(*arg, **kw)
        return func_return
    return wrapper