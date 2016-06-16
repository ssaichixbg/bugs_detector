#!coding=utf-8
import json
import time
import os
import subprocess
from PIL import  Image

from django.shortcuts import render, render_to_response
from django.http.response import *
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic

from .sign import Sign
#from .wxconf import conf

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
exe_path = os.path.join(BASE_DIR, 'bugs.exe')


def generate_js_sign(url):
    wechat = WechatBasic(conf=conf)
    return Sign(wechat.get_jsapi_ticket(), url).sign()

def home(request):
    #generate_js_sign(request.get_full_path())
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

    img = Image.open(os.path.join(path, file_name))
    (x, y) = img.size
    x_s = 1000
    y_s = y * x_s / x
    out = img.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(os.path.join(path, file_name))

    cmd = '%s %s' % (exe_path, os.path.join(path, file_name))
    #p=subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output =''
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
        output = e.output
    count = output
    print cmd
    print count

    return render_to_response('result.html', locals())
