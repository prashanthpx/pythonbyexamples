Excellent question — and yes, in Python, you absolutely can define class or instance attributes dynamically after an object (or even the class itself) is created.

However, it’s important to understand the difference between:

Instance attributes → attached to one specific object

Class attributes → attached to the class itself (shared across all instances)

Let’s go through both cases with detailed examples and nuances 👇

🧩 1️⃣ Dynamically adding instance attributes

You can add new attributes to an individual object anytime — even after it’s created.

class Person:
    def __init__(self, name):
        self.name = name

# Create an instance
p = Person("Alice")

# Dynamically add a new attribute
p.age = 30

print(p.name)  # Alice
print(p.age)   # 30


✅ Works fine — Python simply adds a new key to that object’s internal __dict__.

Check it:

print(p.__dict__)
# {'name': 'Alice', 'age': 30}


🔸 Other instances of Person won’t have this attribute unless you give it to them individually.

q = Person("Bob")
print(hasattr(q, "age"))  # False

🧩 2️⃣ Dynamically adding class attributes (shared across all instances)

You can also add or modify class-level attributes after the class is defined.

class Person:
    pass

# Add a class attribute dynamically
Person.species = "Homo sapiens"

# Works for all instances
p = Person()
print(p.species)  # Homo sapiens


✅ Any instance created before or after will see the same shared class attribute.

q = Person()
print(q.species)  # Homo sapiens


If you change it on the class:

Person.species = "Human"
print(p.species)  # Human
print(q.species)  # Human


But if you change it on one instance, it shadows the class variable for that object only:

p.species = "Cyborg"
print(p.species)  # Cyborg
print(q.species)  # Human

🧠 3️⃣ Using setattr() for dynamic assignment

You can use Python’s built-in setattr() for both instances and classes.

For an instance:
p = Person()
setattr(p, "country", "India")
print(p.country)  # India

For a class:
setattr(Person, "planet", "Earth")
print(p.planet)  # Earth


This is especially handy when adding attributes programmatically (e.g., from a config file, JSON, or reflection).

⚙️ 4️⃣ Dynamically adding methods (not just data)

You can also attach new methods dynamically to:

the class (shared by all instances)

an individual instance (only that object)

Add method to a class:
def greet(self):
    print(f"Hello, my name is {self.name}")

Person.greet = greet

p = Person("Alice")
p.greet()  # Hello, my name is Alice

Add method to a single instance:
import types

def farewell(self):
    print(f"Goodbye from {self.name}")

p.farewell = types.MethodType(farewell, p)
p.farewell()  # Goodbye from Alice


Other instances won’t have farewell() unless you attach it to them too.

🧩 5️⃣ Dynamically adding attributes at creation time (via __init__ kwargs)

Sometimes, you want to dynamically assign attributes based on data given at construction time:

class Person:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

p = Person(name="Alice", age=30, city="Bangalore")
print(p.__dict__)
# {'name': 'Alice', 'age': 30, 'city': 'Bangalore'}

⚠️ Caveats
Situation	Effect
Adding attributes to instances	Works per object only
Adding attributes to class	Shared by all objects (existing + future)
If class uses __slots__	Dynamic attribute creation is not allowed unless __dict__ is defined
Dynamically added methods	Won’t be picked up by static analyzers or type hints

Example of the __slots__ restriction:

class Person:
    __slots__ = ['name']

p = Person()
p.name = "Alice"
p.age = 30  # ❌ AttributeError: 'Person' object has no attribute 'age'

✅ TL;DR Summary
Task	How to do it	Applies to
Add instance attribute dynamically	obj.new_attr = value or setattr(obj, 'new_attr', value)	That specific object only
Add class attribute dynamically	ClassName.new_attr = value or setattr(ClassName, 'new_attr', value)	All instances
Add method dynamically	ClassName.method = func	All instances
Restrict dynamic attributes	Use __slots__	Prevents arbitrary additions

In short:
Yes — Python’s dynamic nature allows adding new attributes (or even methods) at runtime to both classes and objects.
It’s one of Python’s most powerful (and sometimes dangerous) features — use it thoughtfully.