#encoding=utf-8
#http://yuyin.baidu.com/docs/asr/57
#Q：语音识别REST API支持的音频格式、采样率有哪些？
#A：支持的压缩格式有：pcm（不压缩）、wav、opus、speex、amr、x-flac。原始 PCM 的录音参数必须符合 8k/16k 采样率、16bit 位深、单声道。

#Q：语音识别 REST API 最长支持多长的录音？
#A： 最长支持60s的录音文件。对文件大小没有限制，只对时长有限制。
#
import wave
import urllib, urllib2, pycurl
import base64
import json
import StringIO

import weather
import os
## get access token by api key & secret key

def get_token():
    apiKey = "6fBsLcoVxPNCGbka1BqCxnwe"
    secretKey = "b00451f53e93bd7f893886973fd571e3"

    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;

    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']

def dump_res(buf):
    print "dump_res"
    print buf
    response_data = json.loads(buf)
    command = response_data['result'][0].encode("UTF-8")
    if command.find('天气') != -1:
        print 'weather'
        weather.broadcast()
    elif command.find('播放音乐') != -1:
        print 'music'
        os.system('mplayer "%s"' %('./1.mp3'))


## post audio to server
def use_cloud(token):
    fp = wave.open('./test.wav', 'rb')
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)

    cuid = "xxxxxxxxxx" #my xiaomi phone MAC
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
    http_header = [
        'Content-Type: audio/pcm; rate=8000',
        'Content-Length: %d' % f_len
    ]
    b=StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val
    print c.getinfo(pycurl.HTTP_CODE)
    print c.getinfo(c.CONTENT_TYPE)

if __name__ == "__main__":
    token = get_token()
    use_cloud(token)
