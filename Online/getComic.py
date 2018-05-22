#coding:utf-8
#!/usr/bin/python

import json
import requests
from bs4 import BeautifulSoup
import MangagoUtils


addComicApi = 'manga/addFile'
addChapterApi = 'manga/addchapter'

def isNeedUpdate(data):
    index_url = data['mangaUrl']
    count = data['chapterCount']
    try:
        response = requests.get(index_url)
        soup = BeautifulSoup(response.text, "html.parser")
        chapters = soup.select('.chapter')
        if len(chapters) > count:
            print 'id='+str(data['id'])+' 需要更新'
            for i in range(0, len(chapters)-count):
                chapter_url = chapters[i].a['href']
                chapter_title = chapters[i].a.get_text().encode('UTF-8', 'ignore')
                #执行更新方法
                getNettruyenComicChapter(index_url,chapter_url,len(chapters)-i)
                print 'id='+str(data['id'])+'更新章节'+ str(len(chapters)-i) + '完成 标题为：' + chapter_title
        else:
            print 'id='+str(data['id'])+'不需要更新'
    except Exception as e:
        print('Error', e)

def getNettruyenComicChapter(comic_url,chapter_url,position):
    #name 字段放漫画URL
    imgList = []
    try:
        response = requests.get(chapter_url)
        soup = BeautifulSoup(response.text, "html.parser")
        chapter_title = soup.select('.breadcrumb')[0].find_all('span')[3].get_text().encode('UTF-8', 'ignore')
        pages = soup.select('.page-chapter')
        for page in pages:
            imgList.append(page.img['src'].encode('UTF-8', 'ignore'))
        comic_chapter = {'chap_url': chapter_url.encode('UTF-8', 'ignore'), 'chapter_title': chapter_title,'chap_imgs': imgList,'name':comic_url,'position':position}
        info_json = json.dumps(comic_chapter, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8",
                               ensure_ascii=False)
        #print info_json
        file = MangagoUtils.SaveToChapterJson(chapter_title, comic_chapter)
        MangagoUtils.postFiles(file,addChapterApi)
    except Exception as e:
        print('Error', e)

