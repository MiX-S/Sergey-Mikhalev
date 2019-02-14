N = int(input())

numbers = [i for i in range(N + 1)]
prime_numbers = []

for i in range(2, len(numbers)):
    p = numbers[i]
    if p != 0:
        for j in range(2*p, N + 1, p):
            numbers[j] = 0
        prime_numbers.append(p)
        
print(prime_numbers)
