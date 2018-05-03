import requests
from bs4 import BeautifulSoup    
from distutils.filelist import findall
import MySQLdb
import json

#encoding = gbk  
 
url = "http://www.nettruyen.com/truyen-tranh/lac-vao-the-gioi-game"


def getNettruyenComic(chapter_url):
	imgList = []
	try:
		response  = requests.get(chapter_url)
		soup = BeautifulSoup(response.text,"html.parser")    
		#pages = soup.find_all('div','page-chapter') same as bottom 
		pages = soup.select('.page-chapter')
		for page in pages:
			#print page.img['src']
			imgList.append(page.img['src'])  
	except Exception as e:
		print('Error',e)
	return imgList
		
		

def getNettruyenComicIndex(page_url):
	Chapters_List = []
	Tag_List = []
	try:
		response  = requests.get(page_url)
		soup = BeautifulSoup(response.text,"html.parser")
		title_temp = soup.select('.other-name')[0].get_text()
		title = title_temp.encode('GBK', 'ignore');
		#print title
		
		describe_temp = soup.select('.detail-content')[0].p.get_text()
		describe = describe_temp.encode('GBK', 'ignore');
		#print describe
		
		author_temp = soup.select('.col-xs-8')[2].get_text()
		author = author_temp.encode('GBK', 'ignore');
		#print author
		
		cover = soup.select('.col-image')[0].img['src']
		#print cover
		
		status_temp = soup.select('.col-xs-8')[3].get_text()
		status = status_temp.encode('GBK', 'ignore');
		
		tags = soup.select('.col-xs-8')[4].select('a')
		for tag in tags:
			Tag_List.append(tag.get_text().encode('GBK', 'ignore'))
		#print Tag_List
		
		
		createtimes = soup.select('.text-center' '.col-xs-4' '.small')
		
		chapters = soup.select('.chapter')
		for i in range(0, len(chapters)):
			chapter_url = chapters[i].a['href']
			#print chapter_url + " is loading"
			#comic_chapter = {'chap_url':chapter_url,'chap_imgs':getNettruyenComic(chapter_url),'createtime':''}
			comic_chapter = {'chap_url':chapter_url,'chap_imgs':'','createtime':createtimes[i].get_text()}
			Chapters_List.append(comic_chapter)
		info = {'title':title,'describe':describe,'chapter':Chapters_List,'author':author,'cover':cover,'status':status,'tag':Tag_List}
		print json.dumps(info,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True )
	except Exception as e:
		print('Error',e)
		


getNettruyenComicIndex(url)



