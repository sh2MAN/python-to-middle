class LazyMeta:
    def __init__(self, name, bases, namespace):
        super().__init__()

    def __setattr__(self, key, value):
        print(1==1)

    def __call__(self, instance):
        expression = getattr(self, 'expression')
        return expression()


class Lazy(metaclass=LazyMeta):
    def __init__(self, expression) -> None:
        super().__init__()
        object.__setattr__(self, 'expression', expression)


if __name__ == '__main__':
    def return_3():
        print('create')
        return 3

    number = Lazy(return_3)
    first_result = number + 2
