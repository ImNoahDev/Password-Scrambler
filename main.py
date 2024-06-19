from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from random_word import RandomWords
import os
import pyperclip
from flask import Flask, render_template, request

# Create an instance of RandomWords
r = RandomWords()

# Generate words function: Generates 3 random words
def generate_words():
    words = ""
    # Generate 3 random words and capitalize them
    for i in range(3):
        buffer = r.get_random_word() + " "
        words += buffer.capitalize()
    return words

def base64Encoding(input):
    dataBase64 = base64.b64encode(input)
    dataBase64P = dataBase64.decode("UTF-8")
    return dataBase64P

def base64Decoding(input):
    return base64.decodebytes(input.encode("ascii"))

def aesEcbEncryptToBase64(encryptionKey, plaintext):
    cipher = AES.new(encryptionKey, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode("ascii"), AES.block_size))
    return base64Encoding(ciphertext)

def aesEcbDecryptFromBase64(decryptionKey, ciphertextDecryptionBase64):
    ciphertext = base64Decoding(ciphertextDecryptionBase64)
    cipher = AES.new(decryptionKey, AES.MODE_ECB)
    decryptedtext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    decryptedtextP = decryptedtext.decode("UTF-8")
    return decryptedtextP

# Generate a key and save it to a file if it doesn't exist or read it from the file if it exists
def generate_key():
    # Check if key exists
    if os.path.exists("key.key"):
        # Read key from file
        with open("key.key", "rb") as key_file:
            key = key_file.read()
            print("Key already exists! Using old key")
            return key
    else:
        # Generate a new 256-bit (32 bytes) AES key if key doesn't exist
        key = get_random_bytes(32)
        with open("key.key", "wb") as key_file:
            # Write key to file
            key_file.write(key)
            print("No key found, Generating a new key")
            return key

# Encrypt words
def encrypt_words(message, key):
    encrypted = aesEcbEncryptToBase64(key, message)
    return encrypted

# Decrypt words
def decrypt_words(encrypted, key):
    decrypted = aesEcbDecryptFromBase64(key, encrypted)
    return decrypted

# Initialise Flask
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Encrypt route
@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = generate_words()
    key = generate_key()
    encrypted = encrypt_words(message, key)
    encrypted_str = encrypted  # Already a string from aesEcbEncryptToBase64
    # Copy encrypted message to clipboard
    pyperclip.copy(encrypted_str)
    clipboard_message = "Encrypted message copied to clipboard!"
    # Render result page
    return render_template('result.html', message=message, encrypted=encrypted_str, clipboard_message=clipboard_message)

# Decrypt route
@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_str = request.form['encrypted']
    try:
        encrypted_bytes = encrypted_str
        key = generate_key()
        decrypted = encrypt_words(encrypted_bytes, key)
    except Exception as e: # Handle exceptions
        decrypted = f"Error decrypting message: {e}"
    # Render result page
    return render_template('result.html', encrypted=encrypted_str, decrypted=decrypted)

# Run the app
if __name__ == '__main__':
    app.run()
