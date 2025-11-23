def greet_user(first_name, last_name):
	print("hi there")
	print(f"welcome aboard {first_name} {last_name}")

def keyword_arg(first_name, last_name):
	print(f"welcome aboard {first_name} {last_name}")
	

greet_user("Prashanth", "Kumar")
# these are called keyword argument where position of the argument doesn't matter
keyword_arg(last_name="Smith", first_name="John")