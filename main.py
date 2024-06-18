# Import Modules
from cryptography.fernet import Fernet
from random_word import RandomWords
import os

r = RandomWords()

def generate_words():
    words = ""
    for i in range(3):
        buffer = r.get_random_word()
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
            