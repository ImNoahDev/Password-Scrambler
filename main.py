from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from random_word import RandomWords
import pyperclip
from flask import Flask, render_template, request
import secrets

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
    if len(encryptionKey) not in (16, 24, 32):
        raise ValueError("Encryption key must be 16, 24, or 32 bytes long")
    cipher = AES.new(encryptionKey, AES.MODE_ECB)
    padded_text = pad(plaintext.encode("ascii"), AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return base64.b64encode(ciphertext).decode('ascii')

def generate_key():
    # Generate a new 256-bit (32 bytes) AES key
    key = secrets.token_bytes(32)
    # key = str()
    # key = base64Decoding(key)
    print("Generated a new key")
    return key

# Encrypt words
def encrypt_words(message, key):
    return aesEcbEncryptToBase64(key, message)

# Initialise Flask
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = generate_words()
    key = generate_key()
    # print(key) Logging to check if key is working
    encrypted = encrypt_words(message, key)
    encrypted_str = encrypted  
    key = base64Encoding(key)
    # Copy encrypted message to clipboard
    pyperclip.copy(encrypted_str)
    clipboard_message = "Encrypted message copied to clipboard!"

    # Render result page with message, encrypted string, key, and clipboard message
    return render_template('result.html', message=message, encrypted=encrypted, key=key, clipboard_message=clipboard_message)

# Decrypt route
@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_str = str(request.form['encrypted'])
    decryption_key = request.form['decryption_key']  # Get decryption key from form
    decryption_key = base64Decoding(decryption_key)
    # print(decryption_key) Logging to check if key is working

    try:
        decrypted = encrypt_words(encrypted_str, decryption_key)
    except Exception as e:
        decrypted = f"Error decrypting message: {e}"

    return render_template('result.html', encrypted=encrypted_str, decrypted=decrypted)


# Run the app
if __name__ == '__main__':
    app.run()
