#!coding=utf-8
import json
import time
import os
import urllib
import subprocess
from PIL import Image

from django.shortcuts import render, render_to_response
from django.http.response import *


from .sign import generate_js_signature, get_token
from .wxconf import conf

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
exe_path = os.path.join(BASE_DIR, 'bugs.exe')
BASE_HOST = 'http://test.chalaoshi.cn'

def generate_js_sign(url):
    return generate_js_signature(conf['appid'],conf['appsecret'],url,conf['token'])

def wx_js_sign(f):
    def wrap(request):
        request.wx = generate_js_sign(BASE_HOST + request.get_full_path())
        return f(request)

    return wrap

@wx_js_sign
def home(request):
    return render_to_response('index.html')

@wx_js_sign
def detect(request):
    return render_to_response('detect.html', locals())

def get_count(request):
    mid = request.get('media_id')

    url = 'https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' %(get_token(conf['appid'],conf['appsecret']) ,mid)


    path = os.path.join(BASE_DIR, 'static')
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = '%d.jpg' % int(time.time())

    urllib.urlretrieve(url, os.path.join(path, file_name))

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

    return HttpResponse(count)
