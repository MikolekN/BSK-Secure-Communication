import random
import string

import rsa
import os
from hashlib import sha256

import AES


class Key:

    @staticmethod
    def get_public_key(login):
        with open(f"{os.path.curdir}/public_keys/{login}.pem", "r") as f:
            key_data = f.read()
            public_key = rsa.PublicKey.load_pkcs1(key_data.encode('utf8'))
        return public_key

    @staticmethod
    def get_private_key(login, password):
        with open(f"{os.path.curdir}/private_keys/{login}.pem", "r") as f:
            key_data = f.read()
            ciphered_private_key = rsa.PrivateKey.load_pkcs1(key_data.encode('utf8'))
        private_key = AES.AES.deciper(ciphered_private_key, sha256(password.encode()).hexdigest())
        return private_key

    @staticmethod
    def get_keys(login, password):
        return Key.get_public_key(login), Key.get_private_key(login, password)

    @staticmethod
    def check_password(login, password):
        public_key, private_key = Key.get_keys(login, password)
        control_message = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(64))
        returned_message = rsa.decrypt(rsa.encrypt(control_message.encode(), public_key), private_key).decode('utf8')
        return control_message == returned_message

    @staticmethod
    def __set_public_key(login, public_key):
        with open(f"{os.path.curdir}/public_keys/{login}.pem", "w") as f:
            f.write(public_key.save_pkcs1("PEM").decode('utf8'))

    @staticmethod
    def __set_private_key(login, password, private_key):
        ciphered_private_key = AES.AES.ciper(private_key, sha256(password.encode()).hexdigest())
        with open(f"{os.path.curdir}/private_keys/{login}.pem", "w") as f:
            f.write(ciphered_private_key.save_pkcs1("PEM").decode('utf8'))

    @staticmethod
    def set_keys(login, password):
        public_key, private_key = rsa.newkeys(1024)
        Key.__set_public_key(login, public_key)
        Key.__set_private_key(login, password, private_key)
        return True
