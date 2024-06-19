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
    dataBase64 = base64.b64encode(input)
    dataBase64P = dataBase64.decode("UTF-8")
    return dataBase64P

def base64Decoding(input):
    return base64.decodebytes(input.encode("ascii"))

def aesEcbEncryptToBase64(encryptionKey, plaintext):
    cipher = AES.new(encryptionKey, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode("ascii"), AES.block_size))
    return base64Encoding(ciphertext)

def generate_key():
    # Generate a new 256-bit (32 bytes) AES key
    key = secrets.token_bytes(32)
    print("Generated a new key")
    return key

# Encrypt words
def encrypt_words(message, key):
    encrypted = aesEcbEncryptToBase64(key, message)
    return encrypted

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
    encrypted = encrypt_words(message, key)
    encrypted_str = encrypted  # Replace with your actual encrypted message
    key = base64Encoding(key)
    # Copy encrypted message to clipboard
    pyperclip.copy(encrypted_str)
    clipboard_message = "Encrypted message copied to clipboard!"

    # Render result page with message, encrypted string, key, and clipboard message
    return render_template('result.html', message=message, encrypted=encrypted_str, key=key, clipboard_message=clipboard_message)

# Decrypt route
@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_str = request.form['encrypted']
    decryption_key = request.form['decryption_key']  # Get decryption key from form
    decryption_key = base64Decoding(decryption_key)

    try:
        decrypted = encrypt_words(encrypted_str, decryption_key)
    except Exception as e:
        decrypted = f"Error decrypting message: {e}"

    return render_template('result.html', encrypted=encrypted_str, decrypted=decrypted)


# Run the app
if __name__ == '__main__':
    app.run()
