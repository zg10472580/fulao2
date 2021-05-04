import base64
import hashlib
from Crypto.Cipher import AES

# 密钥（key）, 密斯偏移量（iv） CBC模式加密

def AES_Decrypt(key, data):
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据

    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 去补位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted


key = 'db6f7f9e5d7a770e0e3497a7d7a077f5'
x_vtag = '162039286'
vi = hashlib.new('md5', x_vtag.encode("utf-8")).hexdigest()[8:24]
data = 'favicon'
text_decrypted = AES_Decrypt(key, data)
print(text_decrypted)
