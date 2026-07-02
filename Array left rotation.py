def reverse(arr,start,end):
  while start<end:
    temp=arr[start]
    arr[start]=arr[end]
    start+=1
    end-=1
arr=[1,2,3,4,5,6,7]
k=3
n=len(arr)
k=k%n
#Reverse the entire array
reverse(arr,0,k-1)
#Reverse the first n elements
reverse(arr,k,n-1)
#Reverse the remaining elements
reverse(arr,0,n-1)
print("Array after left rotation:")
for num in arr:
  print(num,end=" ")
