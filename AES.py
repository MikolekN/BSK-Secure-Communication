from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import os
"""
AES.py
"""


class AES_algorithm:

    @staticmethod
    def encrypt_message_CBC(message, key):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = iv
        ciphertext += cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        return ciphertext

    @staticmethod
    def decrypt_message_CBC(message, key):
        iv = message[:AES.block_size]
        content = message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(content), AES.block_size).decode('utf-8')
        return plaintext

    @staticmethod
    def encrypt_file_CBC(file_path, key):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        content = b""
        content += iv
        finished = False
        with open(file_path, "rb") as file:
            while not finished:
                chunk = file.read(1024)
                if len(chunk) == 0 or len(chunk) % AES.block_size != 0:  # final block/chunk is padded before encryption
                    padding_length = (AES.block_size - len(chunk) % AES.block_size) or AES.block_size
                    chunk += str.encode(padding_length * chr(padding_length))
                    finished = True
                content += cipher.encrypt(chunk)
            content += b"<END>"
        return content

    @staticmethod
    def decrypt_file_CBC(message, key):
        iv = message[:AES.block_size]
        content = message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = b""
        finished = False
        start = 0
        step = 1024
        end = step
        deciphered_file_bytes = b""
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(content[start:end])
            start = end
            end += step
            if len(next_chunk) == 0:
                padding_length = chunk[-1]
                chunk = chunk[:-padding_length]
                finished = True
            deciphered_file_bytes += chunk
        return deciphered_file_bytes
