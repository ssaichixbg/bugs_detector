import time
import random
import string
import hashlib
import urllib2
import re

def generate_js_signature(appid, appsecret,url, noncestr):
    import time

    # get jsapi_ticket
    token = get_token(appid, appsecret)
    ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%(token)s&type=jsapi'\
          % {'token': token}
    try:
        result = urllib2.urlopen(ticket_url, timeout=20).read()
    except:
        return None
    result = re.findall('"ticket":"(.*?)"', result)
    jsapi_ticket = result[0]

    timestamp = int(time.time())
    sign = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' \
            %(jsapi_ticket,noncestr,timestamp,url)
    sha1result = hashlib.sha1()
    sha1result.update(sign)
    sign = sha1result.hexdigest()

    return {
        'appId':appid,
        'timestamp':timestamp,
        'nonceStr':noncestr,
        'signature':sign,
        'url':url
    }

def get_token(appid, appsecret):
    """
    Get AccessToken by appid and appsecret.The result will be saved in cache for 7000s
    :param appid:
    :param appsecret:
    :return: AccessToekn.
    """
    import time


    url = """https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%(appid)s&secret=%(appsecret)s""" \
        % {'appid': appid, 'appsecret': appsecret}
    result = ''
    try:
        result = urllib2.urlopen(url, timeout=20).read()
    except:
        return None
    result = re.findall('"access_token":"(.*?)"', result)

    return result[0]

