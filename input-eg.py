print(input("whats the best programming language?"))

print(input("whats the comfortable programming language?") + " is the best programming language")

year = input("Enter birth year\n")
# age = 2025 - year # gives error
age = 2025 - int(year)

print(age)
# TypeError: can only concatenate str (not "int") to str
# print("age is " + age)

# printing different data types
print(f"age is  {age}")