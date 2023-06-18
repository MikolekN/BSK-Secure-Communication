import socket
import sys

import rsa
import threading
import os
from time import sleep

import key
from constants import HOST, PORT


class Client:
    login = None
    password = None
    public_key = None
    private_key = None

    sock = None

    server_public_key = None
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
            self.server_public_key = rsa.PublicKey.load_pkcs1(self.sock.recv(1024))
            self.sock.send(self.public_key.save_pkcs1())
            enc_session_key = self.sock.recv(1024)
            self.session_key = rsa.decrypt(enc_session_key, self.private_key)
        except socket.timeout:
            if self.sock is not None:
                self.sock.close()
                self.sock = None
            self.server_public_key = None
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
        self.sock.send("t".encode())
        self.sock.send(message.encode())

    def send_file(self, file_path):
        self.progress_bar_active = True
        self.sock.send("f".encode())
        file_name = os.path.basename(file_path)
        dir_path = os.path.dirname(file_path)
        new_file_path = dir_path + "/new_" + file_name
        file_size = os.path.getsize(file_path)
        message = f"{new_file_path}|{file_size}"
        self.sock.send(message.encode())
        sleep(2)
        parts = int(int(file_size) / 1024) + 1
        percent = 100 / parts
        with open(file_path, "rb") as file:
            while True:
                message = file.read(1024)
                if not message:
                    break
                self.sock.send(message)
                self.progress_bar_value += percent
        self.progress_bar_active = False
        self.progress_bar_value = 0

    def receive_message(self):
        message = self.sock.recv(1024).decode('utf-8')
        if not message:
            return False
        self.messages.append(message)
        return True

    def receive_file(self):
        self.progress_bar_active = True
        message = self.sock.recv(1024)
        file_path, file_size = message.decode('utf-8').split("|")
        file_bytes = b""
        parts = int(int(file_size) / 1024) + 1
        percent = 100 / parts
        while True:
            message = self.sock.recv(1024)
            if not message:
                self.progress_bar_active = False
                self.progress_bar_value = 0
                return False
            file_bytes += message
            if sys.getsizeof(file_bytes) - 33 >= int(file_size):
                break
            self.progress_bar_value += percent
        with open(file_path, "wb") as file:
            file.write(file_bytes)
        self.progress_bar_active = False
        self.progress_bar_value = 0
        return True
