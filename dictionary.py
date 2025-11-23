customer = {
	"name": "kumar",
	"location": "blr",
	"age": 50
}

print(f"customer: {customer['name']}")

# Iterating through key and value
for k, v in customer.items():
	print(f"k: {k}, v: {v}")

# iterating through keys only
for i in customer:
	print(f"i: {i}")
	# Now using i (which is key) to extract data for each key
	print(f"val: {customer[i]}")

# Adding anew key to dictionary
customer["locality"] = "bangalore"

# priting the new key
print(customer["locality"])

# Passing key that doesn't exits
# prints none when using get()
print(customer.get('name1'))

# prints error when accessed directly 
print(customer["n"])


'''
output
prkumar@prkumar--MacBookPro18 pythonexamples % /Users/prkumar/.pyenv/versions/3.9.2/bin/python "/Users/prkumar/Documents/No Backup/pythonexample
s/practice/dictionary.py"
customer: kumar
k: name, v: kumar
k: location, v: blr
k: age, v: 50
i: name
val: kumar
i: location
val: blr
i: age
val: 50
bangalore
None
Traceback (most recent call last):
  File "/Users/prkumar/Documents/No Backup/pythonexamples/practice/dictionary.py", line 30, in <module>
    print(customer["n"])
KeyError: 'n'
'''