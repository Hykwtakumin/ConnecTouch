# -*- coding: utf-8 -*-
#
# NFCを認識したらConnecTouch.orgにリクエストを送出
#
# パソコンの場合はパソコンの利用履歴URLも送出
#

import nfc
import binascii
import requests
from datetime import datetime
from uuid import getnode as get_mac
from subprocess import Popen
import os

readerId = "%012x" % get_mac() # リーダに接続されたマシンのMACアドレス(48ビット整数)のHex値

def lasturl():
    LOGFILE = '/Users/masui/Sites/rememberurl.log'
    loglines = open(LOGFILE).read().split('\n')
    lastline = loglines[len(loglines)-2]
    [time, url] = lastline.split('\t')
    return url

def startup(targets):
    print 'waiting for NFC tag ...'
    return targets

def connected(tag):
    nfcId = binascii.hexlify(tag.identifier)
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print("|%s| readerId: %s nfcId: %s" % (date, readerId, nfcId))
    
    Popen('/home/pi/ConnecTouch/Reader/led.sh',shell=True)

    if readerId == "a45e60e40c05": # 増井のパソコンの場合URLも通知
        request = "http://connectouch.org/addlink/%s/%s?url=%s" % (readerId, nfcId, lasturl())
    else:
        request = "http://connectouch.org/addlink/%s/%s" % (readerId, nfcId)

    try:
        res = requests.get(request)
        print(res.text)
    except Exception, e:
        print(e)

    return id
    
def released(tag):
    print 'released'
    
clf = nfc.ContactlessFrontend('usb')
if clf:
    while clf.connect(rdwr={
            'on-startup': startup,
            'on-connect': connected,
            'on-release': released,
    }):
        pass
    
        
