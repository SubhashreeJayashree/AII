# Fibonacci series of 5 numbers

n = 5
a, b = 0, 1

for i in range(n):
    print(a, end=" ")
    a, b = b, a + b
