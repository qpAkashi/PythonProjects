import random
import string


encryptionChars = list(string.punctuation + string.ascii_letters + string.digits)
print("Original characters:", encryptionChars)


encryptionKey = encryptionChars.copy()
random.shuffle(encryptionKey)
print("Shuffled encryption key:", encryptionKey)


message = input("Enter the message you would like to encrypt: ")


encryptedMessage = ""
for letter in message:
    if letter in encryptionChars:
        index = encryptionChars.index(letter)
        encryptedMessage += encryptionKey[index]
    else:
        encryptedMessage += letter  


print("Encrypted message:", encryptedMessage)