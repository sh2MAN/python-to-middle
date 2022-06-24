from copy import copy, deepcopy


class Updateable(type):
    _instance = None

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        delattributes = []
        for attr in cls.__dict__:
            if attr.startswith('__'):
                continue
            elif attr not in namespace:
                delattributes.append(attr)

        for attr in delattributes:
            delattr(cls, attr)

        for name, val in namespace.items():
            if callable(val):
                setattr(cls, name, val)

    def __new__(cls, name, bases, namespace):
        if not cls._instance:
            cls._instance = super().__new__(cls, name, bases, namespace)
        return cls._instance
