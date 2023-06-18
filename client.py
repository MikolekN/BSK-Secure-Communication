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

    def send_message(self, message, mode):
        message_info = f"t|{mode}"
        ciphered_message_info = AES.AES_algorithm.encrypt_message_CBC(message_info, self.session_key)
        self.sock.send(ciphered_message_info)
        if mode == "ECB":
            ciphered_message = AES.AES_algorithm.encrypt_message_ECB(message, self.session_key)
        elif mode == "CBC":
            ciphered_message = AES.AES_algorithm.encrypt_message_CBC(message, self.session_key)
        else:
            return
        self.sock.send(ciphered_message)

    def send_file(self, file_path, mode):
        message_info = f"f|{mode}"
        ciphered_message_info = AES.AES_algorithm.encrypt_message_CBC(message_info, self.session_key)
        self.sock.send(ciphered_message_info)
        file_name = os.path.basename(file_path)
        dir_path = os.path.dirname(file_path)
        new_file_path = dir_path + "/new_" + file_name
        file_size = os.path.getsize(file_path)
        message = f"{new_file_path}|{file_size}"
        if mode == "ECB":
            ciphered_message = AES.AES_algorithm.encrypt_message_ECB(message, self.session_key)
        elif mode == "CBC":
            ciphered_message = AES.AES_algorithm.encrypt_message_CBC(message, self.session_key)
        else:
            return
        sleep(1)
        self.sock.send(ciphered_message)
        sleep(1)
        if mode == "ECB":
            ciphered_file = AES.AES_algorithm.encrypt_file_ECB(file_path, self.session_key)
        elif mode == "CBC":
            ciphered_file = AES.AES_algorithm.encrypt_file_CBC(file_path, self.session_key)
        else:
            return
        start = 0
        step = 1024
        end = step
        length = sys.getsizeof(ciphered_file) - 33
        while start < length:
            chunk = ciphered_file[start:end]
            self.sock.send(chunk)
            start = end
            end += step

    def receive(self):
        while True:
            ciphered_message_info = self.sock.recv(1024)
            message_info = AES.AES_algorithm.decrypt_message_CBC(ciphered_message_info, self.session_key)
            msg_type, mode = message_info.split("|")
            if not msg_type:
                break
            if msg_type == "t":  # text
                if not self.receive_message(mode):
                    break
            elif msg_type == "f":  # file
                if not self.receive_file(mode):
                    break

    def receive_message(self, mode):
        message = self.sock.recv(1024)
        if not message:
            return False
        if mode == "ECB":
            deciphered_message = AES.AES_algorithm.decrypt_message_ECB(message, self.session_key)
        elif mode == "CBC":
            deciphered_message = AES.AES_algorithm.decrypt_message_CBC(message, self.session_key)
        else:
            return
        self.messages.append(deciphered_message)
        return True

    def receive_file(self, mode):
        message = self.sock.recv(1024)
        if not message:
            return False
        if mode == "ECB":
            deciphered_message = AES.AES_algorithm.decrypt_message_ECB(message, self.session_key)
        elif mode == "CBC":
            deciphered_message = AES.AES_algorithm.decrypt_message_CBC(message, self.session_key)
        else:
            return
        file_path, file_size = deciphered_message.split("|")
        file_bytes = b""
        while True:
            message = self.sock.recv(1024)
            file_bytes += message
            if sys.getsizeof(file_bytes) - 33 >= int(file_size):
                break
        if mode == "ECB":
            deciphered_file_bytes = AES.AES_algorithm.decrypt_file_ECB(file_bytes, self.session_key)
        elif mode == "CBC":
            deciphered_file_bytes = AES.AES_algorithm.decrypt_file_CBC(file_bytes, self.session_key)
        else:
            return
        with open(file_path, "wb") as file:
            file.write(deciphered_file_bytes)
        return True
