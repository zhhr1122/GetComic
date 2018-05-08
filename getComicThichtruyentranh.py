#coding:utf-8
#!/usr/bin/python

from Tkinter import *

import requests
from bs4 import BeautifulSoup
import json
import MangagoUtils
url = 'http://thichtruyentranh.com/huong-mat-tram-tram/huong-mat-tram-tram-chap-1/135312.html?c=1'
base_url = 'http://thichtruyentranh.com'
def getComicThichtruyentranh(chapter_url):
    imgList = []
    try:
        response = requests.get(chapter_url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all('script')[6].get_text().split(';')[0].split('[')[1].split(']')[0].strip().replace("\n", "").split(',')
        for image in images:
            imgList.append(image.strip().split('"')[1])
    except Exception as e:
        print('Error', e)
    return imgList


def getComicThichtruyentranhIndex(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            chapters = soup.select('.ul_listchap')[1].select('a')
        except Exception as e:
            chapters = soup.select('.ul_listchap')[0].select('a')
            print('Error', e)

        for chapter in chapters:
            print base_url+chapter['href']
            #print getComicThichtruyentranh(base_url + chapter['href'])

        try:
            pages = soup.select('.paging')[0].select('a')
            for page in pages:
                page_url = base_url + page['href']
                response = requests.get(page_url)
                soup = BeautifulSoup(response.text, "html.parser")
                chapters = soup.select('.ul_listchap')[1].select('a')
                for chapter in chapters:
                    print base_url + chapter['href']
                    print getComicThichtruyentranh(base_url + chapter['href'])
        except Exception as e:
            print('Error', e)
        print 'success'

    except Exception as e:
        print('Error', e)



getComicThichtruyentranh(url)