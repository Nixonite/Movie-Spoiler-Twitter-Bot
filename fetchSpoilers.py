import urllib2
from BeautifulSoup import BeautifulSoup
import sqlite3

conn = sqlite3.connect('moviespoilerbot.db')
c = conn.cursor()

spoilerSite = 'http://www.spollywood.com/'

def weirdTextFix(str):
	str = str.replace("&amp;","&")#replace stuff with ampersand sign
	str = str.replace("&#39;","''")#replace stuff with 2 single quotes (necessary for sql insertion)
	str = str.replace("(","")
	str = str.replace(")","")
	return str

def getSite():
	return urllib2.urlopen(spoilerSite).read()
	
def getTheDamnText(soupstuff):
	text = str(soupstuff)
	text = text[text.index('>')+1:text.index('</')]
	return text
	
def parsePage(html_page):
	soup = BeautifulSoup(html_page)
	title = soup.findAll(attrs={'class' : 'title-text'})
	spoiler = soup.findAll(attrs={'class':'spoiler-text'})
	title = getTheDamnText(title)
	spoiler = getTheDamnText(spoiler)
	title = weirdTextFix(title)
	spoiler = weirdTextFix(spoiler)
	return (title,spoiler)
	
def insertToDB(title,spoiler):
	valid_utf8 = True #because mysql only takes utf-8 and too lazy to change that, but still runs into problem sometimes? what the hell...
	try:
		title.decode('utf-8')
		spoiler.decode('utf-8')
	except UnicodeDecodeError:
		valid_utf8 = False
	
	if valid_utf8:
		if(len(spoiler)<=140):#to be tweetable
			tablename = "table_"+title[0]
			c.execute("create table if not exists "+tablename+"(ID INTEGER PRIMARY KEY, TITLE text, SPOILER text)")
			conn.commit()
			c.execute("select 1 from "+tablename+" where TITLE=:title",{"title":title})
			conn.commit()
			if c.fetchone() is None:
					c.execute("insert into "+tablename+" (TITLE,SPOILER) values (:title,:spoiler)",{"title":title,"spoiler":spoiler})
					print title
					print spoiler
					conn.commit()
	

for i in range(300):
	t,s = parsePage(getSite())
	insertToDB(t,s)

conn.close()