def f(x):
    if isinstance(x, int):
        return lambda: x
    return -x()

print f(f(-500))