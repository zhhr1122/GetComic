#coding:utf-8
#!/usr/bin/python

import json

import requests
import getComic

import datetime



def getComicList(localid):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    print nowTime +'开始请求更新'
    response = requests.get('http://mangago.in:8088/mangago-bss/manga/selectByLocaleId?localeId='+str(localid))
    json_response = response.content.decode()
    dict_json = json.loads(json_response)
    datas = dict_json['data']
    for data in datas:
       getComic.isNeedUpdate(data)
    print '全部更新完成'

#getComicList(80)