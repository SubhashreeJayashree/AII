# Swapping without using a temporary variable

a = 10
b = 20

a = a + b
b = a - b
a = a - b

print("After swapping:")
print("a =", a)
print("b =", b)
