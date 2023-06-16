import os
import threading
import socket
import rsa
import os

host = '127.0.0.1'
port = 20001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()
clients = []
nicknames = []
public_keys = []

server_public_key, server_private_key = rsa.newkeys(1024)
print(server_public_key)


def generate_session_key(length=32):
    session_key = os.urandom(length)

    return session_key


def broadcast_message(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)


# main function to handle client connection
def handle_client_connection(client):
    while True:
        message = client.recv(1024)
        if not message:
            break
        broadcast_message(message, client)

    client.close()
    index = clients.index(client)
    clients.remove(index)

# the main function to receive client connection


def receive_client_connection():
    session_key = generate_session_key()
    print(f"session_key: {session_key}")
    while True:
        if len(clients) < 2:
            client, address = server.accept()
            client.send(server_public_key.save_pkcs1('PEM'))
            print(f'connection is established with {str(address)}')
            clients.append(client)
            client_public_key = client.recv(1024)
            print(client_public_key)
            public_keys.append(client_public_key)
            enc_session_key = rsa.encrypt(session_key, rsa.PublicKey.load_pkcs1(client_public_key))
            client.send(enc_session_key)
            thread = threading.Thread(target=handle_client_connection, args=(client,))
            thread.start()
            print("Client connected.")


if __name__ == '__main__':
    receive_client_connection()
