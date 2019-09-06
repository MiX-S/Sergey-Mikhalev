def fib(N):
	fib_list = [1, 1]
	if N == 1 or N == 2:
		return 1
	for i in range(2, N):
		fib_list.append(fib_list[i-1] + fib_list[i-2])
	return fib_list[-1]

def fiblist(N):
	fib_list = [1, 1]
	if N == 1 or N == 2:
		return 1
	for i in range(2, N):
		fib_list.append(fib_list[i-1] + fib_list[i-2])
	return fib_list