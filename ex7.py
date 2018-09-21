number = int(input())

def Prime(N):
    for i in range(2, int(N**0.5) + 1):
        if N % i == 0:
            return False
    return True

Prime(number)
