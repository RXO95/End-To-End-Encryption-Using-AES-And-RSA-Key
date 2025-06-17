# End-to-End Encrypted Chat Application (Python)

A secure real-time chat application built using **Python sockets**, **RSA + AES encryption**, and a simple **Tkinter-based GUI**. This project demonstrates how end-to-end encryption works using a hybrid cryptosystem for secure message exchange between two users.

---

##  Features

-  **End-to-End Encryption** (AES for message, RSA for key exchange)
-  **Private messaging** (not broadcast-based)
-  **Real-time chat system** using Python sockets
-  **Secure key exchange** between clients
-  **User-friendly GUI** using Tkinter
-  **Hybrid Encryption Model** (RSA + AES)

---

##  Encryption Model

- **AES (Advanced Encryption Standard)** is used to encrypt the message.
- **RSA (Rivest-Shamir-Adleman)** is used to encrypt the AES key during transmission.
- Ensures full confidentiality of messages even over unsecured networks.

---

##  Tech Stack

-  Python 3.x
-  Tkinter – GUI for chat interface
-  PyCryptodome – for RSA and AES encryption
-  Socket Programming – for client-server communication

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/secure-chat-app.git
cd secure-chat-app
2. Install Dependencies

Make sure you have Python 3 installed, then run:

pip install pycryptodome

3. Run the Server

python server.py

4. Run the Client(s)

Open another terminal for each user and run:

python client.py

---

##  Authors

    Rakshit (RXO95) – GitHub
    Shreya Shinde – GitHub
---
