try:
	age = int(input("age:"))
except ValueError:
	print("invalid input for age")

'''
1. try: block - Attempts to execute potentially risky code:
input("age:") prompts the user to enter their age
int() tries to convert the user's input (a string) into an integer
Stores the result in the age variable
2. except ValueError: block - Catches a specific type of error:
If the user enters something that can't be converted to an integer (like "abc" or "twenty"), Python raises a ValueError
Instead of crashing the program, the except block catches this error
Prints a user-friendly message: "invalid input for age"

Example scenarios:

✅ User enters "25" → Successfully converts to integer 25, no exception
❌ User enters "hello" → Raises ValueError → Prints "invalid input for age"
❌ User enters "12.5" → Raises ValueError → Prints "invalid input for age"
'''