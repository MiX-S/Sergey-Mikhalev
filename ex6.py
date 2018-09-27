N = int(input())
max_number = int(input())
for _ in range(N-1):
    m = int(input())
    if m > max_number:
        max_number = m
print(max_number)