import time

def timeit(f):
    def wrapper(*args, **kwargs):
        ts = time.time()
        result = f(*args, **kwargs)
        te = time.time()

        print(' - %r took: %2.4f sec' % (f.__name__, te-ts))
        return [result, te-ts]
    return wrapper