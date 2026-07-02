n=int(input())
arr=list(map(int,input().split()))
k=int(input())
k=k%n
print(*(arr[-k:]+arr[:-k]))














Output:
7
1 2 3 4 5 6 7
7 6 5 4 3 2 1
