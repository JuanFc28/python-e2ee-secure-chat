#!/usr/bin/env python3

import socket
import threading
import ssl

def client_thread(client_socket, clients, usernames):
    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    print(f"\n[+] User '{username}' connected to the chat")

    for client in clients:
        if client is not client_socket:
            client.sendall(f"\n[+] User '{username}' joined the chat\n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break
            
            if message == "!users":
                client_socket.sendall(f"\n[+] Active users: {', '.join(usernames.values())}\n\n".encode())
                continue

            for client in clients:
                if client is not client_socket:
                    client.sendall(f"{message}\n".encode())

        except:
            break

    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)
    if client_socket in usernames:
        del usernames[client_socket]


def server_program():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((host, port))

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.key")

    server_socket = context.wrap_socket(server_socket, server_side=True)
    server_socket.listen()

    print(f"\n[+] Server listening for incoming TLS connections on {host}:{port}...")

    clients = []
    usernames = {}

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)

        print(f"\n[+] New secure connection established from {address}")
        
        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames))
        thread.daemon = True
        thread.start()

    server_socket.close()

if __name__ == '__main__':
    server_program()
