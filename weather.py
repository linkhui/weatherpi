# -*- coding: utf-8 -*-
import os
import urllib
import urllib2,json
from datetime import date
from os import path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#返回和风天气数据
def get_city_weather(index, search_type=1):
    if search_type == 1:
        search = 'weather'
    elif search_type == 0:
        search = 'attractions'
    else:
        return -1
    heAPI = 'https://free-api.heweather.com/v5/'
    heKey = '和风key'
    url_weather = heAPI + 'forecast'+'?city='+index+'&key='+heKey
    print url_weather
    req = urllib2.Request(url_weather)
    resp = urllib2.urlopen(req)
    context = resp.read()
    weather_json = json.loads(context, encoding='utf-8')
    fp = open("/home/pi/python/weather/test.txt", 'w')
    fp.write(context)
    fp.close()
    if search_type == 1:
        weather = weather_json["HeWeather5"][0]['daily_forecast'][0]
    else:
        weather = weather_json
    return weather
#获取百度语音token
def get_token():
    api_key = "百度语音合成api key"
    sec_key = "百度语音合成secret key"
    url = url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+api_key+"&client_secret="+sec_key
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    context = resp.read().decode('utf-8')
    return json.loads(context)['access_token']
#获取需要的数据
def get_wat():
    city_id = "CN101021200"  #上海徐汇天气代码   
    city_weather = get_city_weather(city_id)
    a= city_weather['tmp']['max']
    b= city_weather['tmp']['min']
    c= city_weather['cond']['txt_d']
    d= city_weather['cond']['txt_n']
    e= city_weather['date']
    f= city_weather['wind']['dir']
    g= city_weather['wind']['sc']
    h= city_weather['pop']
    return "天气预报  今天是 {}   最高温度{} 最低温度{} 日间天气{} 夜间天气{} {}{} 降水概率百分之{}".format(e,a,b,c,d,f,g,h)
token=get_token()
weather=get_wat() 
#tts
url = "http://tsn.baidu.com/text2audio?tex="+weather+"&lan=zh&per=0&pit=1&spd=4&cuid=b827ebcac3a2&ctp=1&tok="+token
#播放
try:
    os.system('/usr/bin/mplayer -ao alsa:device=hw=1,0 "%s"' %(url))
except Exception as e:
    print('Exception',e)