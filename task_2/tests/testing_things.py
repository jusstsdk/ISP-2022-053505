import math

c = 42


def f(x):
    a = 123
    return math.sin(x * a * c)


def add():
    return c + 8.2


def mul(a, b):
    return a * b


class A:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


bytes1 = bytes(b'd\x01S\x00')
bytearr1 = bytearray(bytes1)
bltfunc = len
lst1 = [1, 2, 3, 4]
set1 = set(lst1)
frzset1 = frozenset(lst1)
bool1 = True


def foo(arr):
    a = 10
    s = 0
    d = {"t1": 12, "t2": 15}
    for x in arr:
        s += x
    return s + a, sorted(arr), d


power = lambda num, p: num ** p


class MyClass:
    def __init__(self):
        self.a = 'a'
        self.b = 1


class B:
    pass


class cls1(MyClass, B):
    pass
