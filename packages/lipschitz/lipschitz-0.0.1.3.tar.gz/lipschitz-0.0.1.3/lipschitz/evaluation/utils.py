def multiprocessing_kwargs(func):
    def wrapper(kwargs):
        return func(**kwargs)
    return wrapper