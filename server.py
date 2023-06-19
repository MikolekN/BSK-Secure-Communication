import threading
import socket
import rsa
import os
from constants import HOST, PORT, DISCONNECT_MESSAGE

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()
clients = []


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
        print(message)
        if message == DISCONNECT_MESSAGE.encode():
            clients.remove(client)
            client.close()
            break
        broadcast_message(message, client)


# the main function to receive client connection
def receive_client_connection():
    session_key = generate_session_key()
    print(f"session_key: {session_key}")
    while True:
        if len(clients) < 2:
            client, address = server.accept()
            print(f'connection is established with {str(address)}')
            clients.append(client)
            client_public_key = client.recv(1024)
            print(client_public_key)
            enc_session_key = rsa.encrypt(session_key, rsa.PublicKey.load_pkcs1(client_public_key))
            client.send(enc_session_key)
            thread = threading.Thread(target=handle_client_connection, args=(client,))
            thread.start()
            print("Client connected.")


if __name__ == '__main__':
    receive_client_connection()
