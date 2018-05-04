#coding:utf-8
#!/usr/bin/python

import requests
import threading
from bs4 import BeautifulSoup
import json
from Tkinter import *
import os



#url = "http://www.nettruyen.com/truyen-tranh/lac-vao-the-gioi-game"


url = "http://www.nettruyen.com/truyen-tranh/tay-du-duong-tang-hang-ma"


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


def getNettruyenComicIndex():
    Chapters_List = []
    Tag_List = []
    try:
        index_url = app.var.get()
        file_name = index_url.split('/')[4]
        print(file_name)
        if isSaved(file_name):
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
            status = listinfo[1].get_text().encode('UTF-8', 'ignore')
            tags = listinfo[2].select('a')
            hot = listinfo[3].get_text().encode('UTF-8', 'ignore')
        else:
            title = listinfo[0].get_text().encode('UTF-8', 'ignore')
            author = listinfo[1].get_text().encode('UTF-8', 'ignore');
            status = listinfo[2].get_text().encode('UTF-8', 'ignore')
            tags = listinfo[3].select('a')
            hot = listinfo[4].get_text().encode('UTF-8', 'ignore')



        for tag in tags:
            Tag_List.append(tag.get_text().encode('UTF-8', 'ignore'))
        # print Tag_List

        #createtimes = soup.select('.text-center' '.col-xs-4' '.small')

        chapters = soup.select('.chapter')
        print title + ' has ' + str(len(chapters)) + ' chapters'
        app.t_url.insert(END, title+' has '+str(len(chapters)) + ' chapters\n')
        for i in range(0, len(chapters)):
            chapter_url = chapters[i].a['href']
            print "Chapter " + str(i + 1) + " is loaded"
            app.t_url.insert(END, title+" Chapter " + str(i + 1) + " is loaded\n")
            comic_chapter = {'chap_url': chapter_url.encode('UTF-8', 'ignore'), 'chap_imgs': getNettruyenComic(chapter_url)}
            # comic_chapter = {'chap_url':chapter_url,'chap_imgs':'','createtime':createtimes[i].get_text()}
            Chapters_List.append(comic_chapter)
        info = {'title': title, 'describe': describe, 'chapter': Chapters_List, 'author': author, 'cover': cover,'status': status, 'tag': Tag_List, "hot": hot,'url':index_url}
        info_json = json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False)
        print info_json
        #app.t_url.insert(END, json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False)+"\n")
        SaveToJson(file_name, info)
    except Exception as e:
        print('Error', e)
        app.t_url.insert(END, str(e) + "\n")


def SaveToJson(title, datas):
    #fl = open('json/'+title.decode('utf-8') + '.json', 'w')
    fl = open('json/' + title + '.json', 'w')
    fl.write(json.dumps(datas, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8", ensure_ascii=False))
    fl.close()
    app.t_url1.insert(END, title + ' save success ' + "\n")
    print title + 'save success'

def isSaved(title):
    jsonfiles = 'json/'+ title+'.json'
    print(jsonfiles)
    if os.access(jsonfiles, os.F_OK):
        app.t_url.insert(END, title + ' is exist \n')
        return True
    else:
        print 'is not Exists'
        return False




def start():
    download_thread = threading.Thread(target=getNettruyenComicIndex)
    download_thread.start()

class App(object):
    def __init__(self, master):
        self.t_lable = Label(master,text='请在下方黏贴需要抓取的漫画url',height =2)
        self.t_lable.pack()

        self.f_top = Frame(master)
        self.f_top.pack()

        self.var = StringVar()
        self.e_entry = Entry(self.f_top, textvariable = self.var,width = 120)
        self.e_entry.pack(side = LEFT)

        self.com = Button(self.f_top, text='获取漫画', command=self.getText, height=2)
        self.com.pack(side=RIGHT)

        self.f_text = Frame(master)
        self.f_text.pack(side=LEFT)

        self.t_status = Label(self.f_text,text='正在进行中任务',height =2)
        self.t_status.pack()

        self.t_url = Text(self.f_text, width=65, height=40)
        self.t_url.pack(side=LEFT, fill=Y)
        self.url_scrollbar = Scrollbar(self.f_text)
        self.url_scrollbar.pack(side=RIGHT, fill=Y)
        self.url_scrollbar.config(command=self.t_url.yview)
        self.t_url.config(yscrollcommand=self.url_scrollbar.set)

        self.f_text1 = Frame(master)
        self.f_text1.pack(side=RIGHT)

        self.t_status1 = Label(self.f_text1, text='已经完成任务', height=2)
        self.t_status1.pack()
        self.t_url1 = Text(self.f_text1, width=65, height=40)
        self.t_url1.pack(side=LEFT, fill=Y)
        self.url_scrollbar1 = Scrollbar(self.f_text1)
        self.url_scrollbar1.pack(side=RIGHT, fill=Y)
        self.url_scrollbar1.config(command=self.t_url1.yview)
        self.t_url1.config(yscrollcommand=self.url_scrollbar1.set)

    def getText(self):
        start()
        self.t_url.delete(1.0, END)
        self.t_url.insert(1.0, self.var.get()+'\n')

root = Tk()
root.title('Mangago漫画爬取器')
root.geometry('960x640')
root.resizable(width=False, height=False) #宽不可变, 高可变,默认为True

app = App(root)
root.mainloop()