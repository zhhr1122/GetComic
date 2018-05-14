#coding:utf-8
#!/usr/bin/python

from Tkinter import *

import requests
from bs4 import BeautifulSoup
import json
import MangagoUtils

def getComicTruyentranh(chapter_url):
    imgList = []
    try:
        response = requests.get(chapter_url)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            pages = soup.select('.each-page')[0].select('img')
            for page in pages:
                image_url = page['src']
                image_alt = page['alt']
                # print(image_alt)
                if cmp('', image_alt) == 0:
                    continue
                print(image_url)
                imgList.append(image_url.encode('UTF-8', 'ignore'))
        except Exception as e:
            pages = soup.select('.OtherText')[0].select('img')
            for page in pages:
                image_url = page['src']
                print(image_url)
                imgList.append(image_url.encode('UTF-8', 'ignore'))
        print(imgList)
    except Exception as e:
        print('Error', e)
    return imgList

#getComicTruyentranh('http://truyentranh.net/shokuryou-jinrui/Chap-034')

def getComicTruyentranhIndex(app,index_url):
    Chapters_List = []
    Tag_List = []
    try:
        file_name = index_url.split('/')[3]
        print(file_name)
        if MangagoUtils.isSaved(app, file_name):
            return
        response = requests.get(index_url)
        soup = BeautifulSoup(response.text, "html.parser")
        title_describe = soup.select('.manga-content')[0].get_text().split(':')
        title = soup.select('.title-manga')[0].get_text().encode('UTF-8', 'ignore')
        describe = title_describe[1].encode('UTF-8', 'ignore')
       # print title
        #print describe

        infos = soup.select('.description-update')[0]
        str_info = infos.get_text()
        hots = str_info.replace(' ', '').split(":")[1].splitlines()[1].split(',')
        hot_str = ''
        for hot in hots:
            hot_str = hot_str + '' + hot

        #print hot
        cover = soup.select('.cover-detail')[0].img['src'].encode('UTF-8', 'ignore')
        #print cover
        str_status = str_info.replace(' ', '').split(":")[4].splitlines()[0].encode('UTF-8', 'ignore')
        status = cmp('ĐangCậpNhật...',str_status)
        if status != 0:
            status = 1
        #print(status)
        tags = infos.select('.CateName')
        for tag in tags:
            Tag_List.append(tag['title'].encode('UTF-8', 'ignore'))
            #print(tag['title'])
        chapters = soup.select('.mCustomScrollbar')[0].select('p')
        print title + ' has ' + str(len(chapters)) + ' chapters'
        app.t_url.insert(1.0, title + ' has ' + str(len(chapters)) + ' chapters\n')
        for i in range(0, len(chapters)):
            try:
                print "Chapter " + str(i + 1) + " is loaded"
                app.t_url.insert(1.0, title + " Chapter " + str(i + 1) + " is loaded\n")
                chapter_url = chapters[i].a['href'].encode('UTF-8', 'ignore')
                chapter_title = chapters[i].a['title'].encode('UTF-8', 'ignore')
                comic_chapter = {'chap_url': chapter_url, 'chapter_title': chapter_title,
                                 'chap_imgs': getComicTruyentranh(chapter_url)}
                Chapters_List.append(comic_chapter)
            except Exception as e:
                print('Error', 'please try again,'+e+'is happening')
                break

        info = {'title': title, 'describe': describe, 'chapter': Chapters_List, 'author': '', 'cover': cover,
                'status': status, 'tag': Tag_List, "hot": hot_str.encode('UTF-8', 'ignore'), 'url': index_url.encode('UTF-8', 'ignore'), 'localId': 80}
        info_json = json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8",
                               ensure_ascii=False)
        print info_json
        MangagoUtils.SaveToJson(app, file_name, info)
    except Exception as e:
        print('Error', e)
        app.t_url.insert(1.0, str(e) + "\n")
