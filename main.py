# Import Modules
from cryptography.fernet import Fernet
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

# Generate a key and save it to a file if it doesn't exist or read it from the file if it exists
def generate_key():
    # Check if key exists
    if os.path.exists("key.key"):
            # Read key from file
            with open("key.key", "rb") as key_file:
                key = key_file.read()
                print("Key already exists! Using old key")
                return key
    # Generate a new key if key doesn't exist
    else:
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                # Write key to file
                key_file.write(key)
                print("No key found, Generating a new key")
                return key
            
# Encrypt words
def encrypt_words(message, key):
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    return encrypted

# Decrypt words
def decrypt_words(encrypted, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted

# Initialise Flask
app = Flask(__name__)
# Home route
@app.route('/')
# Home page
def home():
    return render_template('index.html')

# Encrypt route
@app.route('/encrypt', methods=['POST'])
# Encrypt page
def encrypt():
    message = generate_words()
    key = generate_key()
    encrypted = encrypt_words(message, key)
    encrypted_str = encrypted.decode()  # Convert bytes to string
    # Copy encrypted message to clipboard
    pyperclip.copy(encrypted_str)
    clipboard_message = "Encrypted message copied to clipboard!"
    # Render result page
    return render_template('result.html', message=message, encrypted=encrypted_str, clipboard_message=clipboard_message)

# Decrypt route
@app.route('/decrypt', methods=['POST'])
# Decrypt page
def decrypt():
    encrypted_str = request.form['encrypted']
    try:
        encrypted_bytes = encrypted_str
        key = generate_key()
        decrypted = decrypt_words(encrypted_bytes, key)
        # Convert bytes to string
        decrypted = str(decrypted).split("'")[1]
    except Exception as e: # Handle exceptions
        decrypted = f"Error decrypting message: {e}"
    # Render result page
    return render_template('result.html', encrypted=encrypted_str, decrypted=decrypted)

# Run the app
if __name__ == '__main__':
    app.run()