import urllib2
from BeautifulSoup import BeautifulSoup
import sqlite3

conn = sqlite3.connect('moviespoilerbot.db')
c = conn.cursor()

spoilerSite = 'http://www.spollywood.com/'

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
	
	if(len(spoiler)<=140):
		tablename = "table_"+title[0]
		c.execute("create table if not exists "+tablename+"(ID INTEGER PRIMARY KEY, TITLE text, SPOILER text)")
		c.execute("insert into "+tablename+" (TITLE,SPOILER) values (?,?)",[title,spoiler])
		conn.commit()

for i in range(50):
	parsePage(getSite())

conn.close()