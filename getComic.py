#coding:utf-8
#!/usr/bin/python

import json
from Tkinter import *

import requests
from bs4 import BeautifulSoup

import MangagoUtils


def getNettruyenComic(chapter_url):
    imgList = []
    try:
        response = requests.get(chapter_url)
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
    Chapters_List = []
    Tag_List = []
    try:
        file_name = index_url.split('/')[4]
        print(file_name)
        if MangagoUtils.isSaved(app,file_name):
            return
        response = requests.get(index_url)
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
            comic_chapter = {'chap_url': chapter_url.encode('UTF-8', 'ignore'), 'chapter_title':chapter_title,'chap_imgs': getNettruyenComic(chapter_url)}
            #comic_chapter = {'chap_url':chapter_url.encode('UTF-8', 'ignore'),'chap_imgs':''}
            Chapters_List.append(comic_chapter)
        info = {'title': title, 'describe': describe, 'chapter': Chapters_List, 'author': author, 'cover': cover,'status': status, 'tag': Tag_List, "hot": hot_str.encode('UTF-8', 'ignore'),'url':index_url,'localId':80}
        info_json = json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False)
        print info_json
        #app.t_url.insert(END, json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False)+"\n")
        MangagoUtils.SaveToJson(app,file_name, info)
    except Exception as e:
        print('Error', e)
        app.t_url.insert(END, str(e) + "\n")



