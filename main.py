from hashlib import sha256

import AES
from login_window import LoginWindow
from connection_window import ConnectionWindow
from client import Client
import rsa
import os

from Crypto.Protocol.KDF import PBKDF2

log = LoginWindow()
if log.result:
    if log.login is not None and log.password is not None:
        client = Client(log.login, log.password)
        con = ConnectionWindow(client)

"""password = "Hallo"
print(f"Password: {password}")
password_hash = sha256(password.encode()).digest()
print(f"Hash: {password_hash}")
key = PBKDF2(password_hash, b"", dkLen=32)
print(f"Key: {key}")"""
"""public_key, private_key = rsa.newkeys(1024)
public_key = public_key.save_pkcs1("PEM")
print(f"Public key: {public_key}")
ciphered_public_key, tag, nonce = AES.AES_algorithm.encrypt_message(public_key, key)
print(f"Ciphered public key: {ciphered_public_key}")
new_public_key = AES.AES_algorithm.decrypt_message(ciphered_public_key, key, tag, nonce)
print(f"Deciphered public key: {new_public_key}")"""

"""file_path = "C:\\Users\\Mikolaj\\Desktop\\Grupowy\\do zrobienia.txt"
ciphered_file_path = "C:\\Users\\Mikolaj\\Desktop\\Grupowy\\zaszyfrowany do zrobienia.txt"
deciphered_file_path = "C:\\Users\\Mikolaj\\Desktop\\Grupowy\\odszyfrowany do zrobienia.txt"
file_size = os.path.getsize(file_path)
ciphered_file_data = b""
deciphered_file_data = b""
ivs = []
print("reading file...")
with open(file_path, "rb") as file:
    data = file.read(1024)
    while data:
        ciphered_data, iv = AES.AES_algorithm.encrypt_message(data, key)
        ivs.append(iv)
        ciphered_file_data += ciphered_data
        data = file.read(1024)
print("writing file...")
with open(ciphered_file_path, "wb") as file:
    file.write(ciphered_file_data)
print("reading file...")
with open(ciphered_file_path, "rb") as file:
    data = file.read(1024)
    i = 0
    while data:
        deciphered_data, iv = AES.AES_algorithm.decrypt_message(data, key, ivs[i])
        i += 1
        deciphered_file_data += deciphered_data
        data = file.read(1024)
print("writing file...")
with open(deciphered_file_path, "wb") as file:
    file.write(deciphered_file_data)
print("DONE.")"""
