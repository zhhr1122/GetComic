#coding:utf-8
#!/usr/bin/python

import threading
from Tkinter import *

import getComic
import MangagoUtils
import getComicTruyentranh
import getComicThichtruyentranh


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

        self.t_lable1 = Label(master, text='                               请在下方黏贴需要抓取的漫画章节url                                               漫画URL                        漫画章节数',height=2)
        self.t_lable1.pack()

        self.f_top1 = Frame(master)
        self.f_top1.pack()

        self.var1 = StringVar()
        self.e_entry_1 = Entry(self.f_top1, textvariable=self.var1, width=80)
        self.e_entry_1.pack(side=LEFT)

        self.var2 = StringVar()
        self.e_entry_2 = Entry(self.f_top1, textvariable=self.var2, width=20)
        self.e_entry_2.pack(side=LEFT)

        self.var3 = StringVar()
        self.e_entry_3 = Entry(self.f_top1, textvariable=self.var3, width=20)
        self.e_entry_3.pack(side=LEFT)

        self.com1 = Button(self.f_top1, text='获取章节漫画', command=self.getText1, height=2)
        self.com1.pack(side=RIGHT)

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
        start(self)
        self.t_url.insert(1.0, self.var.get()+'\n')

    def getText1(self):
        startChapter(self)
        self.t_url.insert(1.0, self.var1.get() + '\n')


def start(app):
    mkpath = "C:\\json"
    # 调用函数
    MangagoUtils.mkdir(mkpath)
    index_url = app.var.get()
    scource = index_url.split('/')[2]
    print scource
    app.t_url.insert(1.0, 'the comic is from' + scource)
    if cmp(scource, 'www.nettruyen.com') == 0:
        download_thread = threading.Thread(target=getComic.getNettruyenComicIndex, args=(app, index_url,))
        download_thread.start()
    elif cmp(scource, 'truyentranh.net') == 0:
        download_thread = threading.Thread(target=getComicTruyentranh.getComicTruyentranhIndex, args=(app, index_url,))
        download_thread.start()
    elif cmp(scource, 'thichtruyentranh.com') == 0:
        download_thread = threading.Thread(target=getComicThichtruyentranh.getComicThichtruyentranhIndex, args=(app, index_url,))
        download_thread.start()
    else:
        app.t_url.insert(1.0, '无匹配规则')

def startChapter(app):
    mkpath = "C:\\json"
    # 调用函数
    MangagoUtils.mkdir(mkpath)
    index_url = app.var1.get()
    scource = index_url.split('/')[2]
    print scource
    app.t_url.insert(1.0, 'the comic is from' + scource)
    if cmp(scource, 'www.nettruyen.com') == 0:
        download_thread = threading.Thread(target=getComic.getNettruyenComicChapter, args=(app,index_url))
        download_thread.start()
    else:
        app.t_url.insert(1.0, '无匹配规则')

root = Tk()
root.title('Mangago漫画爬取器1.2.3')
root.geometry('960x640')
root.resizable(width=False, height=False) #宽不可变, 高可变,默认为True

app = App(root)
root.mainloop()