#!coding=utf-8
import json
import time
import os
import commands

from django.shortcuts import render, render_to_response
from django.http.response import *
#from wechat_sdk import WechatConf
#from wechat_sdk import WechatBasic

#from .sign import Sign
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
exe_path = os.path.join(BASE_DIR, 'bugs.exe')

# conf = WechatConf(
#         token='your_token',
#         appid='your_appid',
#         appsecret='your_appsecret',
#         encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
#         encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
#         )
#
# def generate_js_sign(url):
#     wechat = WechatBasic(conf=conf)
#     return Sign(wechat.get_jsapi_ticket(), url).sign()

def home(request):
    return render_to_response('index.html')

def get_count(request):
    f = request.FILES.get('pic')
    path = os.path.join(BASE_DIR, 'static')
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = '%d.jpg' % int(time.time())

    with open(os.path.join(path, file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    output = commands.getoutput('%s %s' % (exe_path, path))
    count = int(output)

    return render_to_response('result.html')