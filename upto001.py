# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 14:54:34 2018

@author: 歪克士
"""

from aip import AipSpeech
import json
import requests as rq
import os
import playsound
import wave
from pyaudio import PyAudio,paInt16

""" 你的 百度AI平台 APPID AK SK """
APP_ID = 'APP_ID'
API_KEY = 'APP_KEY'
SECRET_KEY = 'S_K '

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
"""录音"""
framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<TIME*15:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
        os.system('cls')
    save_wave_file('01.wav',my_buf)
    stream.close()

"""录音"""
def luyin():
    my_record()
    print('over')



"""调用百度语音识别"""
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
def shibie():
    get=client.asr(get_file_content('01.wav'), 'wav', 16000, {'lan': 'zh',})
    new=get['result'][0]
    qs=new
    return qs
"""图灵机器人API"""
def tuling(qs):
    link='图灵API前端'+qs+'&key=API的KEY'
    get=rq.post(link)
    p=get.json()
    text=p['text']
    return text

"""调用百度语音合成"""
def hecheng(text):
    result  = client.synthesis(text, 'zh', 1, {'vol': 5,'per': 4,'spd': 4,'pit': 6,})
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
def play():
    filename='auido.mp3'
    playsound.playsound(filename,True)

def dell():
    os.remove('auido.mp3')
    os.remove('01.wav')



luyin()
qs=shibie()
text=tuling(qs)
hecheng(text)
play()
dell()