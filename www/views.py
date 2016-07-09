#!coding=utf-8
import json
import time
import os
import urllib
import urllib2
import json
import subprocess
from PIL import Image

from django.shortcuts import render, render_to_response
from django.http.response import *


from .sign import generate_js_signature, get_token
from .wxconf import conf

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
exe_path = os.path.join(BASE_DIR, 'bugs.exe')
BASE_HOST = 'http://wx.88039986.cn'

def generate_js_sign(url):
    return generate_js_signature(conf['appid'],conf['appsecret'],url,conf['token'])

def wx_js_sign(f):
    def wrap(request):
        request.wx = generate_js_sign(BASE_HOST + request.get_full_path())
        return f(request)

    return wrap

@wx_js_sign
def home(request):
    cookies = request.COOKIES
    if not 'openid' in cookies:
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
              'appid=%s&' \
              'redirect_uri=%s&' \
              'response_type=code&' \
              'scope=snsapi_userinfo&' \
              'state=STATE#wechat_redirect'
        url = url % (
            conf['appid'],
            urllib.quote(BASE_HOST + '/wx_callback'),

        )
        #return HttpResponseRedirect(url)

    return render_to_response('index.html', locals())

@wx_js_sign
def detect(request):
    return render_to_response('detect.html', locals())

def wx_callback(request):
    code = request.GET('code','')
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&' \
          'secret=%s&' \
          'code=%s&' \
          'grant_type=authorization_code'
    url = url % (
        conf['appid'],
        conf['appsecret'],
        code,
    )

    dic = json.loads(urllib2.urlopen(url).read())
    openid = dic['openid']
    access_token = dic['access_token']
    refresh_token = dic['refresh_token']

    url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&' \
          'openid=%s' \
          '&lang=zh_CN'
    url = url % (
        access_token,
        openid
    )
    dic = json.loads(urllib2.urlopen(url).read())

    response = HttpResponseRedirect('/')
    response.set_cookie('openid', openid, expires=3600*1000)
    response.set_cookie('nickname', dic['nickname'], expires=3600*1000)
    response.set_cookie('sex', dic['sex'], expires=3600*1000)
    response.set_cookie('headimgurl', dic['headimgurl'], expires=3600*1000)
    response.set_cookie('nickname', dic['nickname'], expires=3600*1000)

    print openid, dic['nickname']
    return response

def get_count(request):
    mid = request.GET.get('media_id')

    url = 'https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' %(get_token(conf['appid'],conf['appsecret']) ,mid)


    path = os.path.join(BASE_DIR, 'static')
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = '%d.jpg' % int(time.time())

    urllib.urlretrieve(url, os.path.join(path, file_name))

    img = Image.open(os.path.join(path, file_name))

    (w, h) = img.size
    x = request.GET.get('x', '0')
    y = request.GET.get('y', '0')
    width = request.GET.get('width',w)
    height = request.GET.get('height',h)
    region = (max(0,int(x)),max(0,int(y)),int(width),int(height))
    print 'crop', region
    cropImg = img.crop(region)

    cropImg.save(os.path.join(path, file_name))

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
