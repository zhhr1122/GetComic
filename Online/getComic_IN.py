#coding:utf-8
#!/usr/bin/python

import json
import requests
from bs4 import BeautifulSoup
import MangagoUtils
import logging


addComicApi = 'manga/addFile'
addChapterApi = 'manga/addchapter'

def isNeedUpdate(data):
    index_url = data['mangaUrl']
    count = data['chapterCount']
    try:
        response = requests.get(index_url)
        soup = BeautifulSoup(response.text, "html.parser")
        chapters = soup.select('.chapter-title-rtl')
        if len(chapters) > count:
            logging.info('id='+str(data['id'])+' 需要更新')
            print 'id='+str(data['id'])+' 需要更新'
            for i in range(0, len(chapters)-count):
                chapter_url = chapters[len(chapters)-count-i-1].a['href']
                chapter_title = chapters[len(chapters)-count-i-1].a.get_text().encode('UTF-8', 'ignore')
                getKomikgueComicChapter(index_url, chapter_url,chapter_title, count + i + 1, data['id'])
                logging.info('id=' + str(data['id']) + '更新章节' + str(count + i + 1) + '完成 标题为：' + chapter_title)
                print 'id=' + str(data['id']) + '更新章节' + str(count + i + 1) + '完成 标题为：' + chapter_title
        else:
            logging.info('id='+str(data['id'])+'不需要更新')
            print 'id='+str(data['id'])+'不需要更新'
    except Exception as e:
        logging.error(e.message)
        print('Error', e)


def getKomikgueComicChapter(comic_url,chapter_url,chapter_title,position,id):
    #name 字段放漫画URL
    imgList = []
    try:
        response = requests.get(chapter_url)
        soup = BeautifulSoup(response.text, "html.parser")
        pages = soup.find_all('div', 'col-xs-12 col-sm-12')[0].select('img')
        #print pages
        for page in pages:
            try:
                imgList.append(page['data-src'].encode('UTF-8', 'ignore'))
            except Exception as e:
                print '获取漫画成功'
        comic_chapter = {'chap_url': chapter_url.encode('UTF-8', 'ignore'), 'chapter_title': chapter_title,'chap_imgs': imgList,'name':comic_url,'position':position}
        info_json = json.dumps(comic_chapter, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8",
                               ensure_ascii=False)
        #print info_json
        file = MangagoUtils.SaveToChapterJson(str(id) + '_' + chapter_title, comic_chapter)
        MangagoUtils.postFiles(file, addChapterApi)
    except Exception as e:
        logging.error(e.message)
        print('Error', e)

#getKomikgueComicChapter('https://www.komikgue.com/manga/slam-dunk','https://www.komikgue.com/manga/slam-dunk/222/1','Slam Dunk 222 ',221,532)