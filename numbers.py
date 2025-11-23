import math

x = -2.9
print(abs(x))

print(math.ceil(x))
print(math.floor(x))

numbers = [5, 2, 9, 6, 1]

# printing index of number 6
print(numbers.index(6))

# This gives error as 100   
# print(numbers.index(100))

print(100 in numbers)

# copying a list
number2 = numbers.copy()
number2.append(100)
print(number2)

# removing duplicates
dups = [2, 2, 5, 5, 9, 6, 1, 7, 1, 8, 9, 9]
unique = []
for no in dups:
    if no not in unique:
        unique.append(no)
    
print(f"unique numbers: {unique}")
print(unique)

# sorting the numbers
'''
Calls the .sort() method on the  unique list
The .sort() method sorts the list in-place (modifies the original list)
Important: .sort() returns None, not the sorted list
So  sortn is assigned None
'''
unique.sort()
print(f"sorted numbers: {unique}")

'''
output
2.9
-2
-3
3
Traceback (most recent call last):
  File "/Users/prkumar/Documents/No Backup/pythonexamples/practice/numbers.py", line 15, in <module>
    print(numbers.index(100))
ValueError: 100 is not in list
'''