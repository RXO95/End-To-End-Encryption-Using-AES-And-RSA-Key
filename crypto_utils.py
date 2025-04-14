from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import base64
import os

# Generate RSA key pair
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Encrypt AES key using RSA public key
def encrypt_aes_key(aes_key, recipient_public_key):
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(recipient_public_key))
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return encrypted_aes_key

# Decrypt AES key using RSA private key
def decrypt_aes_key(encrypted_aes_key, private_key):
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    return aes_key

# Encrypt message using AES
def encrypt_message(message, aes_key):
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())
    return cipher_aes.nonce + tag + ciphertext  # Concatenate nonce, tag, and ciphertext

# Decrypt message using AES
def decrypt_message(encrypted_message, aes_key):
    nonce = encrypted_message[:16]
    tag = encrypted_message[16:32]
    ciphertext = encrypted_message[32:]
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    decrypted_message = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return decrypted_message.decode()
