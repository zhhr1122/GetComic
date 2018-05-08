#coding:utf-8
#!/usr/bin/python

from Tkinter import *

import requests
from bs4 import BeautifulSoup
import json
import MangagoUtils
url = 'http://thichtruyentranh.com/huong-mat-tram-tram/6146.html'
base_url = 'http://thichtruyentranh.com'
def getComicThichtruyentranh(chapter_url):
    imgList = []
    try:
        response = requests.get(chapter_url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all('script')[6].get_text().split(';')[0].split('[')[1].split(']')[0].strip().replace("\n", "").split(',')
        for image in images:
            imgList.append(image.strip().split('"')[1].encode('UTF-8', 'ignore'))
    except Exception as e:
        print('Error', e)
    return imgList


def getComicThichtruyentranhIndex(app,index_url):
    Chapters_List = []
    Tag_List = []
    try:
        file_name = index_url.split('/')[3]
        print(file_name)
        if MangagoUtils.isSaved(app, file_name):
            return
        response = requests.get(index_url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select('.spantile2')[0].get_text().encode('UTF-8', 'ignore')
        describe = soup.select('.ulpro_line')[0].select('p')[1].get_text().encode('UTF-8', 'ignore')
        infos = soup.select('.ullist_item')[0].select('li')
        author = infos[0].select('.item2')[0].get_text().strip().split(':')[1].encode('UTF-8', 'ignore')
        hot = infos[4].select('.item2')[0].get_text().strip().split(':')[1].encode('UTF-8', 'ignore')
        status_str = infos[3].select('.item2')[0].get_text().strip().split(':')[1]
        print(status_str)
        if cmp(' Còn Tiếp',status_str.encode('UTF-8', 'ignore')) == 0:
            status = 0
        else:
            status = 1
        tags = infos[1].select('.item2')[0].select('a')
        for tag in tags:
            Tag_List.append(tag.get_text().encode('UTF-8', 'ignore'))

        try:
            chapters = soup.select('.ul_listchap')[1].select('a')
        except Exception as e:
            chapters = soup.select('.ul_listchap')[0].select('a')
            print('Error', e)

        cover = soup.select('.divthum2')[0].select('img')[0]['src'].encode('UTF-8', 'ignore')
        app.t_url.insert(END, title + ' has ' + str(len(chapters)) + ' chapters\n')
        i=0
        for chapter in chapters:
            i += 1
            #print base_url+chapter['href']
            chapter_url = base_url + chapter['href']
            chapter_title = chapter['title']
            app.t_url.insert(END, title + " Chapter " + str(i) + " is loaded\n")
            comic_chapter = {'chap_url': chapter_url.encode('UTF-8', 'ignore'), 'chapter_title': chapter_title.encode('UTF-8', 'ignore'),
                             'chap_imgs': getComicThichtruyentranh(chapter_url)}
            Chapters_List.append(comic_chapter)

        try:
            pages = soup.select('.paging')[0].select('a')
            for page in pages:
                page_url = base_url + page['href']
                response = requests.get(page_url)
                soup = BeautifulSoup(response.text, "html.parser")
                chapters = soup.select('.ul_listchap')[1].select('a')
                for chapter in chapters:
                    i += 1
                    chapter_url = base_url + chapter['href']
                    chapter_title = chapter['title']
                    app.t_url.insert(END, title + " Chapter " + str(i) + " is loaded\n")
                    comic_chapter = {'chap_url': chapter_url.encode('UTF-8', 'ignore'), 'chapter_title': chapter_title.encode('UTF-8', 'ignore'),
                                     'chap_imgs': getComicThichtruyentranh(chapter_url)}
                    Chapters_List.append(comic_chapter)
        except Exception as e:
            print('Error', e)

        info = {'title': title, 'describe': describe, 'chapter': Chapters_List, 'author': author, 'cover': cover,
                'status': status, 'tag': Tag_List, "hot": hot, 'url': index_url,
                'localId': 80}
        info_json = json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8",
                               ensure_ascii=False)
        print info_json

        MangagoUtils.SaveToJson(app, file_name, info)

    except Exception as e:
        print('Error', e)
