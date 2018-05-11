#coding:utf-8
#!/usr/bin/python

import json
from Tkinter import *

import requests
from bs4 import BeautifulSoup
import MangagoUtils
from random import choice
import switchip

uas = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]
headers2 = {"Accept": "text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Referer": "",
            "User-Agent": choice(uas),
            }


def getNettruyenComic(chapter_url,mProxies):
    imgList = []
    try:
        response = requests.get(chapter_url,headers=headers2,proxies=mProxies)
        soup = BeautifulSoup(response.text, "html.parser")
        # pages = soup.find_all('div','page-chapter') same as bottom
        pages = soup.select('.page-chapter')
        for page in pages:
            # print page.img['src']
            imgList.append(page.img['src'].encode('UTF-8', 'ignore'))
    except Exception as e:
        print('Error', e)
    return imgList


def getNettruyenComicIndex(app,index_url):
    mProxies = switchip.get_ip()
    Chapters_List = []
    Tag_List = []
    try:
        file_name = index_url.split('/')[4]
        print(file_name)
        if MangagoUtils.isSaved(app,file_name):
            return
        response = requests.get(index_url,proxies=mProxies)
        print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        listinfo = soup.select('.list-info')[0].select('.col-xs-8')

        # print title

        describe_temp = soup.select('.detail-content')[0].p.get_text()
        describe = describe_temp.encode('UTF-8', 'ignore');
        # print describe

        cover = soup.select('.col-image')[0].img['src'].encode('UTF-8', 'ignore')
        # print cover
        if len(listinfo) == 4:
            title = soup.select('.title-detail')[0].get_text().encode('UTF-8', 'ignore')
            author = listinfo[0].get_text().encode('UTF-8', 'ignore');
            status =  cmp('Đang tiến hành',listinfo[1].get_text().encode('UTF-8', 'ignore'))
            tags = listinfo[2].select('a')
            hots = listinfo[3].get_text().split('.')
            hot_str = ''
            for hot in hots:
                hot_str = hot_str + ''+ hot

        else:
            title = listinfo[0].get_text().encode('UTF-8', 'ignore')
            author = listinfo[1].get_text().encode('UTF-8', 'ignore');
            status = cmp('Đang tiến hành', listinfo[2].get_text().encode('UTF-8', 'ignore'))
            tags = listinfo[3].select('a')
            hots = listinfo[4].get_text().split('.')
            hot_str = ''
            for hot in hots:
                hot_str = hot_str + '' + hot



        for tag in tags:
            Tag_List.append(tag.get_text().encode('UTF-8', 'ignore'))
        # print Tag_List

        #createtimes = soup.select('.text-center' '.col-xs-4' '.small')

        chapters = soup.select('.chapter')
        print title + ' has ' + str(len(chapters)) + ' chapters'
        app.t_url.insert(END, title+' has '+str(len(chapters)) + ' chapters\n')
        for i in range(0, len(chapters)):
            chapter_url = chapters[i].a['href']
            chapter_title = chapters[i].a.get_text().encode('UTF-8', 'ignore')
            print "Chapter " + str(i + 1) + " is loaded"
            app.t_url.insert(END, title+" Chapter " + str(i + 1) + " is loaded\n")
            comic_chapter = {'chap_url': chapter_url.encode('UTF-8', 'ignore'), 'chapter_title':chapter_title,'chap_imgs': getNettruyenComic(chapter_url,mProxies)}
            #comic_chapter = {'chap_url':chapter_url.encode('UTF-8', 'ignore'),'chap_imgs':''}
            Chapters_List.append(comic_chapter)
        info = {'title': title, 'describe': describe, 'chapter': Chapters_List, 'author': author, 'cover': cover,'status': status, 'tag': Tag_List, "hot": hot_str.encode('UTF-8', 'ignore'),'url':index_url,'localId':80}
        info_json = json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False)
        print info_json
        #app.t_url.insert(END, json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False)+"\n")
        MangagoUtils.SaveToJson(app,file_name, info)
    except Exception as e:
        print('Error', e)
        getNettruyenComicIndex(app, index_url)
        app.t_url.insert(END, 'is reloading' + "\n")



