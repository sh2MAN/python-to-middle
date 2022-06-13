import weakref


class MyObject:

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


def cache(func):

    def wrapper(name):
        if not hasattr(func, '_cache'):
            wrapper._cache = weakref.WeakValueDictionary()

        if name not in wrapper._cache:
            obj = func(name)
            wrapper._cache[name] = obj

        return wrapper._cache[name]

    return wrapper


@cache
def create_object(name):
    return MyObject(name)
