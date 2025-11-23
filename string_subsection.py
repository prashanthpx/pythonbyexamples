mystring = "Hello World Python"

print(mystring[0:5]) # first word from 0 to 4th
print(mystring[6:11]) # second word from 6 to 10
print(mystring[12:18]) # third word from 12 to 17

print(mystring[0:2]) # first two characters

print(mystring[3:]) # from 3rd character to end

print(mystring[:8]) # from start to 7th character

# step size - here 2 is step size
print(mystring[::2]) # from start to end with step size 2

# Get hold of the last char in the string using negative indexing
print(mystring[::-1]) # reverse the string

print(mystring[1:-1])

print(len(mystring))

# convert to upper case using upper() method
print(mystring.upper())

# Index of char "W"
print(mystring.find('W'))

# This will not replace the content of mystring
print(mystring.replace("Python", "Golang"))

print(mystring)
'''
output
% python string_subsection.py
World
Python
He
lo World Python
Hello Wo
HloWrdPto
nohtyP dlroW olleH
ello World Pytho
18
18
HELLO WORLD PYTHON
6
Hello World Golang
Hello World Python
'''