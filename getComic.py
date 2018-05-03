import requests
from bs4 import BeautifulSoup    
from distutils.filelist import findall
import MySQLdb
import json

#encoding = gbk  
 
url = "http://www.nettruyen.com/truyen-tranh/lac-vao-the-gioi-game"
#url = "http://www.nettruyen.com/truyen-tranh/tay-du-duong-tang-hang-ma"



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
		
		listinfo = soup.select('.list-info')[0].select('.col-xs-8')
		
		title = listinfo[0].get_text().encode('GBK', 'ignore')
		#print title
		
		describe_temp = soup.select('.detail-content')[0].p.get_text()
		describe = describe_temp.encode('GBK', 'ignore');
		#print describe
		
		author = listinfo[1].get_text().encode('GBK', 'ignore');
		#print author
		
		cover = soup.select('.col-image')[0].img['src']
		#print cover
		if len(listinfo) == 4:
			status = ''
			tags = listinfo[2].select('a')
			hot = listinfo[3].get_text().encode('GBK', 'ignore')
		else:
			status = listinfo[2].get_text().encode('GBK', 'ignore')
			tags = listinfo[3].select('a')
			hot = listinfo[4].get_text().encode('GBK', 'ignore')
			
		
		for tag in tags:
			Tag_List.append(tag.get_text().encode('GBK', 'ignore'))
		#print Tag_List
		
		
		createtimes = soup.select('.text-center' '.col-xs-4' '.small')
		
		chapters = soup.select('.chapter')
		print title +' has ' + str(len(chapters)) + ' chapters'
		for i in range(0, len(chapters)):
			chapter_url = chapters[i].a['href']
			print "Chapter "+str(i+1) + " is loaded"
			#comic_chapter = {'chap_url':chapter_url,'chap_imgs':getNettruyenComic(chapter_url),'createtime':createtimes[i].get_text()}
			comic_chapter = {'chap_url':chapter_url,'chap_imgs':'','createtime':createtimes[i].get_text()}
			Chapters_List.append(comic_chapter)
		info = {'title':title,'describe':describe,'chapter':Chapters_List,'author':author,'cover':cover,'status':status,'tag':Tag_List,"hot":hot}
		print json.dumps(info,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True )
	except Exception as e:
		print('Error',e)
		


getNettruyenComicIndex(url)



