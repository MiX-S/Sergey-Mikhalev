print("I am module lists.py")

def add(l1, l2):
    return [a + b for a, b in zip(l1, l2)]

def sub(l1, l2):
    return [a - b for a, b in zip(l1, l2)]

def _reflect(num):
    return int(str(num)[::-1])

def reflect(l):
    return [_reflect(a) for a in l]
