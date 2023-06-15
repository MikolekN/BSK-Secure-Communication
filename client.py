import socket
import rsa
import threading

import key


class Client:
    host = '127.0.0.1'
    port = 20001

    login = None
    password = None
    public_key = None
    private_key = None

    sock = None

    server_public_key = None
    session_key = None

    receive_thread = None
    send_thread = None

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
            self.sock.connect((self.host, self.port))
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
        pass

    def send_message(self, message):
        self.sock.send("t".encode())
        self.sock.send(message.encode())

    def receive_message(self):
        message = self.sock.recv(1024).decode('utf-8')
        return message

    def send_file(self):
        pass

    def receive_file(self):
        pass
