numbertoreadbale = {
	"1": "one",
	"2": "two",
	"3": "three",
	"4": "four",
	"5": "five",
	"6": "six",
	"7": "severn",
	"8": "eight",
	"9": "nine",
	"0": "zero"
}

inp = input("Enter a number")

output = ""
for n in inp:
	# If n is NOT found (like if someone enters a letter or special character), 
    # it returns the default value "!" instead of crashing with a KeyError
	output += numbertoreadbale.get(n, "!") + " "

print(output)