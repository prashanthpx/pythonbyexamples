iterator = [5, 2, 5, 2, 2]

for item in iterator:
    out = ''
    for val in range(item):
        out += "*"
    print(out)

# Another way of writing the same
print("\n")
for item in iterator:
    print("*" * item)