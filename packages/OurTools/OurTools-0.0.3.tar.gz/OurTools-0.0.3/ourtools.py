# pip install line_profiler
from line_profiler import LineProfiler
from functools import wraps

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