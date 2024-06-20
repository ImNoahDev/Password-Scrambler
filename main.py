# This code generates a random message, encrypts it using AES ECB mode, and displays the encrypted message and key on the result page. 
# It also allows the user to decrypt the message using the key and displays the decrypted message on the result page.

# Import required libraries
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from random_word import RandomWords
import pyperclip
from flask import Flask, render_template, request
import secrets
import waitress

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
    return base64.b64encode(input).decode("UTF-8")

def base64Decoding(input):
    return base64.b64decode(input.encode("UTF-8"))

def aesEcbEncryptToBase64(encryptionKey, plaintext):
    # Check if the encryption key is 16, 24, or 32 bytes long
    if len(encryptionKey) not in (16, 24, 32):
        raise ValueError("Encryption key must be 16, 24, or 32 bytes long")
    cipher = AES.new(encryptionKey, AES.MODE_ECB) # Create a new AES cipher object
    padded_text = pad(plaintext.encode("UTF-8"), AES.block_size) # Pad the plaintext to be a multiple of 16 bytes
    ciphertext = cipher.encrypt(padded_text) # Encrypt the padded plaintext
    return base64.b64encode(ciphertext).decode('UTF-8') # Return the encrypted ciphertext as a base64-encoded string

def generate_key():
    key = secrets.token_bytes(32) # Generate a new 256-bit (32 bytes) AES key
    print("Generated a new key!")
    return key

# Initialise Flask
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html') # Render the index.html template


@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Generate random words and key
    message = generate_words()
    key = generate_key()
    # Encrypt the message
    encrypted = aesEcbEncryptToBase64(key, message)  
    key = base64Encoding(key)
    # Copy encrypted message to clipboard
    pyperclip.copy(encrypted)
    clipboard_message = "Encrypted message copied to clipboard!"
    encrypted=encrypted[0:20] # Display only first 20 characters of encrypted message
    # Render result page with message, encrypted string, key, and clipboard message
    return render_template('result.html', message=message, encrypted=encrypted, key=key, clipboard_message=clipboard_message) 

# Decrypt route
@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_str = str(request.form['encrypted'])
    decryption_key = request.form['decryption_key']  # Get decryption key from form
    decryption_key = base64Decoding(decryption_key)
    # Decrypt the message
    try:
        decrypted = aesEcbEncryptToBase64(decryption_key, encrypted_str)
    except Exception as e:
        decrypted = f"Error decrypting message: {e}"
    decrypted = decrypted[0:20] # Display only first 20 characters of decrypted message
    return render_template('result.html', encrypted=encrypted_str, decrypted=decrypted) # Render result page with message and decrypted strings


# Run the app
if __name__ == '__main__':
    print("Starting server...")
    print("server availible at http://localhost:8080.")
    waitress.serve(app, host='0.0.0.0', port=8080) # Run the app on localhost:8080
