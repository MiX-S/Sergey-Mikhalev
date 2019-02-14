a = int(input())
b = int(input())
c = int(input())

D = b**2 - 4*a*c
if D > 0:
    x1, x2 = (-b - D**0.5)/(2*a), (-b + D**0.5)/(2*a)
    print(x1, x2)
elif D == 0:
    x = -b/(2*a)
    print(x)
else:
    print('нет корней')
