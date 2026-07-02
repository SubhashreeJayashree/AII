n = int(input())
arr = list(map(int, input().split()))
k = int(input())

# Handle cases where k is greater than the array length
k = k % n

# Left rotation slice
print(*(arr[k:] + arr[:k]))
