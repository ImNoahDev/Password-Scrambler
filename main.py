# Import Modules
from cryptography.fernet import Fernet
from random_word import RandomWords
import os
import pyperclip

r = RandomWords()

def generate_words():
    words = ""
    for i in range(3):
        buffer = r.get_random_word() + " "
        words += buffer.capitalize()
    return words

def generate_key():
    if os.path.exists("key.key"):
            with open("key.key", "rb") as key_file:
                key = key_file.read()
                print("Key already exists! Using old key")
                return key
    else:
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)
                print("No key found, Generating a new key")
                return key
            
def encrypt_words(message, key):
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    return encrypted

def decrypt_words(encrypted, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted


key = generate_key()
message = generate_words()

if input("Generate new words? (y/n): ") == "y":
    message = generate_words()
    print(f"Generated words: {message}")
    encrypted = encrypt_words(message, key)
    encrypted = str(encrypted).split("'")[1]
    print(f"Encrypted words: {encrypted}")
    pyperclip.copy(encrypted)
    print("Copied to clipboard!")
else:
     print(str(decrypt_words(input("words to decrypt: "), key)).split("'")[1])