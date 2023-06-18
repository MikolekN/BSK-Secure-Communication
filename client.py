import socket
import sys

import rsa
import threading
import os
from time import sleep

import AES
import key
from constants import HOST, PORT


class Client:
    login = None
    password = None
    public_key = None
    private_key = None

    sock = None

    session_key = None

    receive_thread = None
    send_thread = None

    messages = []
    progress_bar_active = False
    progress_bar_value = 0

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.public_key, self.private_key = key.Key.get_keys(self.login, self.password)

    # Łączenie klienta z serwerem.
    # Zawiera wszystkie potrzebne akcje od utworzenia socketa do otrzymania klucza sesyjnego.
    # Powinno zwracać wartość bool określającą czy nawiązanie połączenia zakończyło się pomyślnie czy nie.
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.sock.send(self.public_key.save_pkcs1())
            enc_session_key = self.sock.recv(1024)
            self.session_key = rsa.decrypt(enc_session_key, self.private_key)
        except socket.timeout:
            if self.sock is not None:
                self.sock.close()
                self.sock = None
            self.session_key = None
            return False
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        return True

    # Zerwanie połączenia z serwerem.
    def disconnect(self):
        pass

    # Ogólne otrzymywanie wiadomości i plików
    def receive(self):
        while True:
            msg_type = self.sock.recv(1024).decode()
            if not msg_type:
                break
            if msg_type == "t":  # text
                if not self.receive_message():
                    break
            elif msg_type == "f":  # file
                if not self.receive_file():
                    break

    def send_message(self, message):
        self.sock.send("t".encode('utf-8'))
        ciphered_message = AES.AES_algorithm.encrypt_message_CBC(message, self.session_key)
        self.sock.send(ciphered_message)

    def send_file(self, file_path):
        self.sock.send("f".encode('utf-8'))
        file_name = os.path.basename(file_path)
        dir_path = os.path.dirname(file_path)
        new_file_path = dir_path + "/new_" + file_name
        file_size = os.path.getsize(file_path)
        message = f"{new_file_path}|{file_size}"
        ciphered_message = AES.AES_algorithm.encrypt_message_CBC(message, self.session_key)
        sleep(1)
        self.sock.send(ciphered_message)
        sleep(1)
        ciphered_file = AES.AES_algorithm.encrypt_file_CBC(file_path, self.session_key)
        start = 0
        step = 1024
        end = step
        length = sys.getsizeof(ciphered_file) - 33
        while start < length:
            chunk = ciphered_file[start:end]
            self.sock.send(chunk)
            start = end
            end += step

    def receive_message(self):
        message = self.sock.recv(1024)
        if not message:
            return False
        deciphered_message = AES.AES_algorithm.decrypt_message_CBC(message, self.session_key)
        self.messages.append(deciphered_message)
        return True

    def receive_file(self):
        message = self.sock.recv(1024)
        if not message:
            return False
        deciphered_message = AES.AES_algorithm.decrypt_message_CBC(message, self.session_key)
        file_path, file_size = deciphered_message.split("|")
        file_bytes = b""
        while True:
            message = self.sock.recv(1024)
            file_bytes += message
            """if sys.getsizeof(file_bytes) - 33 >= int(file_size):
                break"""
            if message[-5:] == b"<END>":
                break
        file_bytes = file_bytes[:-5]
        deciphered_file_bytes = AES.AES_algorithm.decrypt_file_CBC(file_bytes, self.session_key)
        with open(file_path, "wb") as file:
            file.write(deciphered_file_bytes)
        return True
