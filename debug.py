import time

def timer(func):
    def warp(*args, **kwargs):
        start = time.time()
        print(f"{func.__qualname__}:")
        res = func(*args, **kwargs)
        end = time.time()
        print(f"{end-start:.3f} s")
        return res 
    return warp

def debug(func):
    def warp(*args, **kwargs):
        print(f"{func.__qualname__}:")
        res = func(*args, **kwargs)
        print(res)
        return res 
    return warp