# Secure Multi-Client Chat (Python + SSL/TLS Socket Layer)

A multi-threaded client-server chat application implemented in Python utilizing low-level network **Sockets** wrapped within an **SSL/TLS cryptographic layer**. The project provides encrypted data transit over the network, active session management, and a graphical user interface (GUI) built with **Tkinter**.

![Demo del Chat](captura_chat.jpeg)

## Key Features

- **Transport Layer Security (TLS/SSL):** Full symmetric and asymmetric cryptographic wrapping prevents eavesdropping, packet tampering, and man-in-the-middle (MitM) attacks.
- **Concurrent Client Architecture:** Utilizes non-blocking daemon threads (`threading`) to handle simultaneous bidirectional message broadcasting.
- **Graphical User Interface:** Lightweight desktop client featuring auto-scrolling chat history, input handling, and active session controls.
- **Dynamic Control Commands:** Real-time client enumeration (`!users`) and network broadcast notifications on connection state changes.

---

## Cryptographic Handshake & Transport Flow

The communication security model relies on hybrid cryptography established during the TLS socket wrapping phase:

```text
  Client                                                          Server
    |                                                               |
    | ----- (1) TCP 3-Way Handshake (SYN, SYN-ACK, ACK) ----------> |
    |                                                               |
    | ----- (2) ClientHello (Supported Cipher Suites & TLS) ------> |
    | <---- (3) ServerHello + X.509 Certificate (Public Key RSA) -- |
    |                                                               |
    | [Client verifies cert & generates Master Secret]              |
    | ----- (4) Key Exchange (Encrypted Premaster with RSA) ------> |
    |                                                               |
    | [Both derive symmetric session keys: AES-GCM / AES-CBC]       |
    | <===========================================================> |
    |         (5) Bi-directional Encrypted Traffic (AES)            |
```
Transport Initialization: Standard TCP stream establishment via AF_INET / SOCK_STREAM.

Asymmetric Key Exchange (RSA 2048-bit): The server presents its X.509 certificate. The client utilizes the server's public key to securely negotiate a shared secret.

Symmetric Encryption (AES): All subsequent message payloads, commands, and broadcast streams are encrypted and decrypted in memory using symmetric session keys.

## Prerequisites

* Python 3.10+
* OpenSSL CLI (for cryptographic key and X.509 certificate generation)
* Tkinter (sudo apt-get install python3-tk on Debian/Ubuntu systems)


## Instalation and Setup

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/JuanFc28/python-e2ee-secure-chat.git
cd python-e2ee-secure-chat
```
### 2.Generate Local TLS Certificates

Run the following OpenSSL commands to generate the self-signed certificate and private key.

  Note: Private key files (.key) are sensitive and omitted from version control.

```bash
# 1. Generate RSA 2048-bit private key
openssl genpkey -algorithm RSA -out server-key.key -aes256

# 2. Generate Certificate Signing Request (CSR)
openssl req -new -key server-key.key -out server.csr

# 3. Generate self-signed X.509 certificate valid for 365 days
openssl x509 -req -days 365 -in server.csr -signkey server-key.key -out server-cert.pem

# 4. Remove passphrase from the private key for automated script loading
openssl rsa -in server-key.key -out server-key.key
```

## Use

### Start the Secure Server

```bash
python3 server.py
```
### Launch Client Instances
Open separate terminal sessions to simulate multiple participants:
```bash
python3 client.py
```

## Security & Architecture Notes

- Certificate Authority (CA) Validation: The client configuration is set to ssl.CERT_NONE to facilitate local development with self-signed certificates. In production enterprise deployments, host verification should be enforced (ssl.CERT_REQUIRED) against a trusted Root CA.
- Memory Safety: Message payloads are decrypted solely in the client runtime memory before being rendered into the GUI widget.
