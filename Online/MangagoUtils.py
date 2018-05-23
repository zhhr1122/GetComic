#coding:utf-8
#!/usr/bin/python

import json
import requests
import logging

local_url = 'http://188.188.188.149:8080/mangago-bss/'
test_url = 'http://222.129.17.186:18082/mangago-bss/'
online_url = 'http://mangago.in:8088/mangago-bss/'

url = online_url;

def SaveToChapterJson(title, datas):
    fl = open('../../json/' + title + '.json', 'w')
    fl.write(json.dumps(datas, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False))
    fl.close()
    logging.info(title + ' save success')
    print title + ' save success'
    return '../../json/' + title + '.json'


def postFiles(file,api):
    file_url = url+api
    data = {
        'name': 'mangago'
    }
    files = {'file': open(file, 'rb')}
    response = requests.post(file_url, data=data, files=files)
    logging.info(response)
    print response

#postFiles('../../json/lv-999-no-murabito.json','manga/addFile')