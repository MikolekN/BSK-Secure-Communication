from hashlib import sha256

import AES
from login_window import LoginWindow
from connection_window import ConnectionWindow
from client import Client
import rsa

from Crypto.Protocol.KDF import PBKDF2

log = LoginWindow()
if log.result:
    if log.login is not None and log.password is not None:
        client = Client(log.login, log.password)
        con = ConnectionWindow()

"""password = "HasloHallo123456"
key = PBKDF2(password, b"", dkLen=32)
#hash = sha256(password.encode()).hexdigest()
public_key, private_key = rsa.newkeys(1024)
public_key = public_key.save_pkcs1("PEM")
print(f"Key: {public_key}")
ciphered_public_key, tag, nonce = AES.AES_algorithm.encrypt_message(public_key, key)
print(f"Ciphered key: {ciphered_public_key}")
new_public_key = AES.AES_algorithm.decrypt_message(ciphered_public_key, key, tag, nonce)
print(f"Deciphered key: {new_public_key}")"""

