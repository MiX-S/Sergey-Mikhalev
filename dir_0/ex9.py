N, t = map(int, input().split())
A = list(map(int, input().split()))
count = 0

# Prefix sums
pref = []
pref.append(0)
for n in A:
    pref.append(pref[-1] + n)
    
for i in range(len(A)):
    for j in range(i, len(A)):
        sum_substr = pref[j + 1] - pref[i]
        if sum_substr < t:
            count += 1
            
print(count)
