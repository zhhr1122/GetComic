#coding:utf-8
#!/usr/bin/python

import json

import requests
import getComic
import logging
import datetime
import getComic_IN



def getComicList(localid):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # 现在
    logging.basicConfig(filename='../../log/'+nowTime+'_'+str(localid)+'.log', filemode="w", level=logging.DEBUG)
    logging.info(nowTime +'开始请求更新'+str(localid))
    print nowTime +'开始请求更新'
    response = requests.get('http://mangago.in:8088/mangago-bss/manga/selectByLocaleId?localeId='+str(localid))
    json_response = response.content.decode()
    dict_json = json.loads(json_response)
    datas = dict_json['data']
    for data in datas:
        if localid==80:
            getComic.isNeedUpdate(data)
        else:
            getComic_IN.isNeedUpdate(data)
    logging.info('全部更新完成')
    print '全部更新完成'

#getComicList(30)