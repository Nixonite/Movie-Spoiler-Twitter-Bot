import urllib2
from BeautifulSoup import BeautifulSoup
import sqlite3
import re

conn = sqlite3.connect('moviespoilerbot.db')
c = conn.cursor()

spoilerSite = 'http://www.spollywood.com/'

def weirdTextFix(str):
	str = str.replace("&amp;","&")#replace stuff with ampersand sign
	str = str.replace("&#39;","''")#replace stuff with 2 single quotes (necessary for sql insertion)
	return str

def getSite():
	return urllib2.urlopen(spoilerSite).read()
	
def parsePage(html_page):
	soup = BeautifulSoup(html_page)
	title = soup.findAll(attrs={'class' : 'title-text'})
	title = str(title)
	title = title[title.index('>')+1:title.index('</')]
	spoiler = soup.findAll(attrs={'class':'spoiler-text'})
	spoiler = str(spoiler)
	spoiler = spoiler[spoiler.index('>')+1:spoiler.index('</')]
	title = weirdTextFix(title)
	spoiler = weirdTextFix(spoiler)
	print title
	print spoiler
	
	if(len(spoiler)<=140):#to be tweetable
		tablename = "table_"+title[0]
		c.execute("create table if not exists "+tablename+"(ID INTEGER PRIMARY KEY, TITLE text, SPOILER text)")
		c.execute("insert into "+tablename+" (TITLE,SPOILER) values (?,?)",[title,spoiler])
		conn.commit()

for i in range(5):
	parsePage(getSite())

conn.close()