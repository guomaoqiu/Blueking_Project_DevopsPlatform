# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class prpcrypt():
    '''
    @note: 加密解密
    '''
    def __init__(self, key):
        self.key = self.key_length(key)
        self.mode = AES.MODE_CBC

    def key_length(self,data):
        length = 16
        count = len(data)
        add = length - (count % length)
        data = data + ('\0' * add)
        return data

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        textadd = self.key_length(text)
        return b2a_hex(cryptor.encrypt(textadd))

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
