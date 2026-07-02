str1 = input().strip()
str2 = input().strip()

# Fast fail: if lengths don't match, they can't be anagrams
if len(str1) != len(str2):
    print("Not an Anagram")
# If lengths match, then we spend the time to sort and compare
elif sorted(str1) == sorted(str2):
    print("Anagram")
else:
    print("Not an Anagram")



str1 = input("Enter 1st str").lower
str2 = input().strip("Enter 2nd str").lower

# If lengths match, then we spend the time to sort and compare
if sorted(str1) == sorted(str2):
    print("Anagram")
else:
    print("Not an Anagram")




Output:
silent
listen
Anagram
