#!/usr/bin/env python
# coding:utf-8

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


class AESCipher(object):
    """
    require pycrypto
    """
    def __init__(self):
        key = "MrWind-CIA"
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = AESCipher._pad(str(raw))
        iv = Random.new().read(AES.block_size)
        aes_cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.urlsafe_b64encode(iv + aes_cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.urlsafe_b64decode(str(enc))
        iv = enc[:16]
        aes_cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(aes_cipher.decrypt(enc[16:]))

    @staticmethod
    def _pad(s):
        block_size = 16
        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class BaseCodeCipher(object):
    @staticmethod
    def encrypt(raw):
        iv = Random.new().read(2)
        return base64.urlsafe_b64encode(iv + str(raw))

    @staticmethod
    def decrypt(enc):
        dec = base64.urlsafe_b64decode(str(enc))
        return dec[2:]

cipher = BaseCodeCipher()

# Usage
if __name__ == '__main__':
    print cipher.encrypt("7771104")
    print cipher.decrypt(cipher.encrypt("7771104"))
