import re
import hashlib
import base64
import requests
from Crypto.Cipher import AES



"""
url = "https://tv-al.yonghuajz.cn/media/480/130970.m3u8?expire=1618785451&hash=3818aa03efe546aeb706f4ac856e35ee"
response = requests.get(url)
x_vtag = response.headers["x-vtag"]
print(x_vtag)
iv = hashlib.new('md5', x_vtag.encode("utf-8")).hexdigest()[8:24]
text_decrypted = AES_Decrypt(response)
with open("a.m3u8","a")as f:
    f.write(text_decrypted)
"""

# for pasel_m3u8 in open('a.m3u8' , 'r').readlines():
#     if "#EXT-X-KEY:METHOD=AES-128" in pasel_m3u8:
#         print(pasel_m3u8)

# data = open('a.m3u8' , 'r').read()
# url = "https://tv-al.yonghuajz.cn/media/480/130970.m3u8?expire=1618785451&hash=3818aa03efe546aeb706f4ac856e35ee"




class My_M3u8():
    def __init__(self):
        self.headers = {
            # "referer" : "http://www.qq.com",
            "user-agent":"Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36"
          }
        self.Ts_List = []

    def get_m3u8(self , url):
        '''
        请求并解析m3u8
        :param url:
        :return:
        '''

        response = requests.get(url)
        x_vtag = response.headers["x-vtag"]
        vi = hashlib.new('md5', x_vtag.encode("utf-8")).hexdigest()[8:24]
        text_decrypted = self.AES_Decrypt(response.text , vi)

        analysis_tsa = url.split('/')
        self.JieXi(analysis_tsa, text_decrypted)

    # 密钥（key）, 密斯偏移量（iv） CBC模式加密

    def AES_Decrypt(self , data , iv):
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)
        # 将加密数据转换位bytes类型数据

        cipher = AES.new(b"db6f7f9e5d7a770e0e3497a7d7a077f5", AES.MODE_CBC, iv.encode('utf8'))
        text_decrypted = cipher.decrypt(encodebytes)
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)
        # 去补位
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    def JieXi(self , analysis_tsc, response):
        global keys
        if "EXT-X-STREAM-INF" in response:
            m3u8 = re.findall('\n(.*?\.m3u8)', response)[0]
            d = m3u8[0]
            if d == "/":  # 有/
                url = "/".join(analysis_tsc[0:3]) + m3u8
                self.get_m3u8(url)
            elif d != "/":  # 没有/
                url = "/".join(analysis_tsc[0:-1]) + "/" + m3u8
                self.get_m3u8(url)

        elif "#EXT-X-TARGETDURATION" in response:
            ts_list = response.split("\n")
            for ts in ts_list:
                if ".ts" in ts:
                    l = ts[0]
                    if l == "/":  # 有/ 只加域名
                        ts_url = "/".join(analysis_tsc[0:3]) + ts
                        self.Ts_List.append(ts_url)

                    elif "http" in ts:
                        self.Ts_List.append(ts)


                    elif l != "/":  # 没有/
                        ts_url = "/".join(analysis_tsc[0:-1]) + "/" + ts
                        self.Ts_List.append(ts_url)
        if "#EXT-X-KEY" in response:
            for ky in response.split("\n"):
                if "#EXT-X-KEY" in ky:
                    print(ky)
                    kdy = re.findall('URI="(.*?)"', ky)[0]
                    d = kdy[0]
                    if d == "h":
                        url = kdy
                    elif d == "/":  # 有/
                        url = "/".join(analysis_tsc[0:3]) + kdy
                    elif d != "/":  # 没有/
                        url = "/".join(analysis_tsc[0:-1]) + "/" + kdy

                    print('此视频经过加密')
                    print(url)
                    keys = requests.get(url, headers = self.headers).content
                    print(keys)

    def download(self , file_name):

        with open(file_name + ".mp4", "wb")as fff:
            i = 0
            len_i = len(self.Ts_List)
            for _ts_ in self.Ts_List:
                i += 1
                print(_ts_)

                for _ in range(20):
                    try:
                        res = requests.get(_ts_, headers=self.headers)
                        break
                    except:
                        print("重试中。。。")
                        continue
                if len(keys) > 10:
                    cryptor = AES.new(keys, AES.MODE_CBC, keys)
                    fff.write(cryptor.decrypt(res.content))  # 将解密后的视频写入文件
                else:
                    fff.write(res.content)
                print("下载完成，剩余{}，ts总数{}".format(len_i - i, len_i))


M3u8 = My_M3u8()
M3u8.get_m3u8("https:\/\/tv-as.kenmingtech.com\/media\/480\/127303.m3u8?expire=1619055095&hash=e5334e334d6b05d767cbabebb2318f9d")
if M3u8.Ts_List:
    M3u8.download("niubi0.mo4")