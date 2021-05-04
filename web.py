import os
import time
import json
import base64
import hashlib
import requests
from Crypto.Cipher import AES
from flask import Flask , render_template , request

app = Flask(__name__)
gs = {}
@app.route('/')
def index():
    video_url = request.args.get("video_url")
    url_type = request.args.get("url_type")
    vp = request.args.get("vp")
    if video_url:
        #https://tv-as.jinrijujia.com/media/240/65173.m3u8?expire=1619894288&hash=f7e79e3265bc56fabacda422dcd09beb
        print(gs)
        url = gs[str(url_type)] + "/media/" + vp +"/" +  video_url.split("/")[-1]
        return render_template('play.html' , abc = url)

    return render_template('index.html' )

def AES_Decrypt(data , key , vi):
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据

    cipher = AES.new(key, AES.MODE_CBC, vi)
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 去补位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted
    
def get_host():
    url_list = ["https://storage.szkcst.cn/host_f2_2.txt" , "https://www.bjmhkjgs.cn/host_f2_2.txt" , "https://storage.yzsxtc.com/host_f2_2.txt" , "https://d3lffz6e701n7t.cloudfront.net/host_f2_2.txt"]
    for url in url_list:
        try:
            data = requests.get(url).text
            with open("host.json" , "w+")as f:
                f.write(data)
            return
        except:
            pass

def host_main():
    is_file = os.path.exists("host.json")
    if (is_file == False):
        get_host()
    else:
        file_time = os.path.getctime("host.json")
        sy = time.time() - file_time
        if sy > float(172800000):
            get_host()
    k = base64.b64decode('nmApNwff9C569lnYpy9zi76KGG5evLfR+m+2gMixKzo=')
    iv = base64.b64decode("39+1jNW7m4BLBRBz7xDxHA==")
    file_data = open("host.json")
    text_decrypted = AES_Decrypt(file_data.read() , k , iv)[32:-32]
    file_data.close()
    data = json.loads(text_decrypted)['stream']
    for i in range(1,4):
        gs[str(i)] = data[i]['url']

@app.route('/lfj')
def play():
    m = request.args.get("m")
    m3u8 = base64.b64decode(m)
    response = requests.get(m3u8)
    x_vtag = response.headers['x-vtag']
    iv = hashlib.new('md5', x_vtag.encode("utf-8")).hexdigest()[8:24]
    return AES_Decrypt(response.text , 'db6f7f9e5d7a770e0e3497a7d7a077f5'.encode('utf8') , iv.encode('utf8'))


if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    host_main()
    app.run(
        host = "0.0.0.0",
        port = 3360
    )