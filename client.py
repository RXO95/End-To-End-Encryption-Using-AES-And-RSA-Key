import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import os

# Generate unique RSA keys for each client
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

username = input("Enter your username: ")
client.send(username.encode())  # Send username to server

# Send public key to the server
client.send(public_key)
print(f"Sent public key for {username}")

# Dictionary to store public keys of other clients
public_keys = {}

def send_message():
    recipient = recipient_entry.get()
    message = message_entry.get()

    if recipient in public_keys:
        aes_key = os.urandom(16)  # Generate AES session key
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_keys[recipient]))
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)

        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())

        encrypted_payload = encrypted_aes_key + cipher_aes.nonce + tag + ciphertext
        client.send(recipient.encode() + b'||' + encrypted_payload)

        chat_box.insert(tk.END, f"You (to {recipient}): {message}\n")
    else:
        chat_box.insert(tk.END, "Public key not found for recipient.\n")

def receive_messages():
    global public_keys
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            
            try:
                # Update public keys if received as a dictionary
                updated_keys = eval(data.decode())
                if isinstance(updated_keys, dict):
                    public_keys = updated_keys
                    print(f"Received public keys: {public_keys}")
                    continue
            except:
                pass

            # Extract encrypted AES key, nonce, tag, and ciphertext
            encrypted_aes_key = data[:256]
            nonce = data[256:272]
            tag = data[272:288]
            ciphertext = data[288:]

            cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
            aes_key = cipher_rsa.decrypt(encrypted_aes_key)

            cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
            decrypted_message = cipher_aes.decrypt_and_verify(ciphertext, tag).decode()

            chat_box.insert(tk.END, f"Received: {decrypted_message}\n")
        except:
            break

# GUI Setup
root = tk.Tk()
root.title(f"Secure Chat - {username}")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
chat_box.pack(padx=10, pady=10)

recipient_entry = tk.Entry(root, width=30)
recipient_entry.pack()
recipient_entry.insert(0, "Enter recipient username")

message_entry = tk.Entry(root, width=50)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
