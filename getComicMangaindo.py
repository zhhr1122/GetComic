#coding:utf-8
#!/usr/bin/python

import json
from Tkinter import *

import requests
from bs4 import BeautifulSoup
import MangagoUtils

def getMangaindoComic(chapter_url):
    imgList = []
    try:
        response = requests.get(chapter_url)
        soup = BeautifulSoup(response.text, "html.parser")
        # pages = soup.find_all('div','page-chapter') same as bottom
        #print soup
        pages = soup.find_all('div','col-xs-12 col-sm-12')[0].select('img')
        #print pages
        for page in pages:
            imgList.append(page['data-src'].encode('UTF-8', 'ignore'))
        print imgList
    except Exception as e:
        print imgList
    return imgList



def getMangaindoComicIndex(app,index_url):
    Chapters_List = []
    Tag_List = []
    try:
        file_name = index_url.split('/')[4]
        print(file_name)
        if MangagoUtils.isSaved(app,file_name):
            return
        response = requests.get(index_url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select('.widget-title')[0].get_text()
        author = soup.select('.dl-horizontal')[0].select('dd')[4].get_text().strip()
        tags = soup.select('.dl-horizontal')[0].select('dd')[7].select('a')
        for tag in tags:
            Tag_List.append(tag.get_text())
        hot = soup.select('.dl-horizontal')[0].select('dd')[8].get_text()
        status = cmp('Ongoing',soup.select('.dl-horizontal')[0].select('dd')[2].get_text().strip())
        cover = soup.select('.img-responsive')[0]['src']
        describe = soup.select('.col-lg-12')[0].p.get_text()
        chapters = soup.select('.chapter-title-rtl')
        app.t_url.insert(1.0, title + ' has ' + str(len(chapters)) + ' chapters\n')
        for i in range(0, len(chapters)):
            app.t_url.insert(1.0, title + " Chapter " + str(i + 1) + "/" + str(len(chapters)) + "\n")
            chapter_url = chapters[i].a['href']
            chapter_title = chapters[i].a.get_text()
            print "Chapter " + str(i + 1) + " is loaded"
            comic_chapter = {'chap_url': chapter_url.encode('UTF-8', 'ignore'), 'chapter_title': chapter_title,
                             'chap_imgs': getMangaindoComic(chapter_url)}
            Chapters_List.append(comic_chapter)
        info = {'title': title, 'describe': describe, 'chapter': Chapters_List, 'author': author, 'cover': cover,'status': status, 'tag': Tag_List, "hot": hot.encode('UTF-8', 'ignore'),'url':index_url,'localId':30}
        info_json = json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False)
        print info_json
        app.t_url.insert(1.0, json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False)+"\n")
        MangagoUtils.SaveToJson(app,file_name, info)
    except Exception as e:
        print('Error', e)
        app.t_url.insert(1.0, e)


