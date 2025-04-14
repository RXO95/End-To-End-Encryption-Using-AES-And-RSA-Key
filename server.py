import socket
import threading
from Crypto.PublicKey import RSA

# Store client connections and public keys
clients = {}
public_keys = {}

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5555))
server.listen()

def handle_client(client, username):
    try:
        # Receive the public key
        public_key = client.recv(2048)
        public_keys[username] = public_key  # Store public key
        print(f"Stored public keys: {public_keys.keys()}")

        # Send updated public keys to all clients
        for c in clients.values():
            c.sendall(str(public_keys).encode())

        while True:
            data = client.recv(4096)
            if not data:
                break

            # Extract recipient and encrypted message
            recipient, encrypted_message = data.split(b'||', 1)

            recipient = recipient.decode()
            if recipient in clients:
                clients[recipient].sendall(encrypted_message)
            else:
                print(f"Recipient {recipient} not found.")
    except Exception as e:
        print(f"Error handling {username}: {e}")
    finally:
        print(f"{username} disconnected.")
        del clients[username]
        del public_keys[username]
        client.close()

print("Server waiting for connections...")

while True:
    client, addr = server.accept()
    username = client.recv(1024).decode()
    clients[username] = client
    print(f"New user connected: {username} from {addr}")

    threading.Thread(target=handle_client, args=(client, username)).start()
