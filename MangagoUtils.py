#coding:utf-8
#!/usr/bin/python

import json
from Tkinter import *
import os
import requests

def SaveToJson(app,title, datas):
    #fl = open('json/'+title.decode('utf-8') + '.json', 'w')
    fl = open('C:/json/' + title + '.json', 'w')
    fl.write(json.dumps(datas, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False))
    fl.close()
    print postFiles('C:/json/' + title + '.json')
    app.t_url1.insert(END, title + ' save success ' + "\n")
    print title + 'save success'


def postFiles(file):
    data = {
        'name': 'mangago'
    }
    files = {'file': open(file, 'rb')}
    response = requests.post('http://222.129.17.186:18082/mangago-bss/manga/addFile', data=data, files=files)
    return response


def isSaved(app,title):
    jsonfiles = 'c:/json/'+ title+'.json'
    print(jsonfiles)
    if os.access(jsonfiles, os.F_OK):
        app.t_url.insert(END, title + ' is exist \n')
        return True
    else:
        print 'is not Exists'
        return False

def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + ' 目录已存在'
        return False