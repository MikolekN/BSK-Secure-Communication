from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
"""
AES.py
"""


class AES_algorithm:

    @staticmethod
    def encrypt_message(message, key):
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message, AES.block_size))
        return ciphertext, cipher.iv

    @staticmethod
    def encrypt_message_EAX(message, key):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(message)
        return ciphertext, cipher.nonce, tag

    @staticmethod
    def decrypt_message(message, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(message), AES.block_size)
        return plaintext

    @staticmethod
    def decrypt_message_EAX(message, key, nonce, tag):
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        plaintext = cipher.decrypt_and_verify(message, tag)
        return plaintext

    @staticmethod
    def encrypt_file(message, key):
        raise NotImplemented

    @staticmethod
    def decrypt_file(message, key):
        raise NotImplemented
