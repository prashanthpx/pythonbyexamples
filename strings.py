message = input(">")
words = message.split(' ')
emojis = {
    ":)": "😊",
    ":(": "😒"
}

output = ""
for word in words:
    # The problem is that emojis.get(word) returns None when the word is
    #  not found in the dictionary, which will cause a 
    # TypeError when trying to concatenate it to a string.
    # output += emojis.get(word) + " " ---> wrong
    # second parameter of get() is the default value to return if the key is not found
    output += emojis.get(word, word) + " "
print(output)