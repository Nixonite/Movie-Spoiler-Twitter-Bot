from nltk.stem.lancaster import LancasterStemmer
import pymongo
import re
import sqlite3


def toRegex(movie):
	regex = "(?i)"
	for i in movie:
		if i == " ":
			regex+= "(\s)?"
		else:
			regex+= i
	return regex

def mongoConnect():
	try:
		conn = pymongo.MongoClient()
		db = conn.twitter
		twitterDB = db.lines
		return twitterDB
	except IOError:
		print "Can't connect to either mongo or the twitter db."	

def genRegex(movies):
	movieRegex = []
	for i in movies:
		movieRegex.append(toRegex(i))
	return movieRegex
		
def genMoviesRegexTuple(movies,movieRegex):
	movieAndRegex = []
	for i in range(len(movies)):
		movieAndRegex.append((movies[i],movieRegex[i]))
	return movieAndRegex

def sqlStart():
	try:
		return sqlite3.connect('moviespoilerbot.db')
	except IOError:
		print "Can't connect to sql db called moviespoilerbot.db"

def sqlConnect(SQLCONN):	
	return SQLCONN.cursor()
	
def sqlClose(SQLCONN):
	SQLCONN.close()

def regexFilter(tweet):
	if re.search("(?i)watched|saw|again|seen|watches|was|great|fantastic|amazing|cool|good|went",tweet['text']) is None:
		if re.search("(?i)watch|watching|wanna|see|want",tweet['text']):		
			return True
		else: return False
	else: return False

def spoil(tweet,movieAndRegex,sqlc):
	tablename = "table_"+movieAndRegex[0][0]
	sqlc.execute("select spoiler from "+tablename+" where TITLE=:title",{"title":movieAndRegex[0]})
	spoiler = sqlc.fetchone()
	print tweet['id_str'],tweet['text'],"\n","Movie:",movieAndRegex[0],"\t Spoiler:",spoiler,"\n\n\n"

def query(movieAndRegex,twitterDB=mongoConnect(),sqlc=sqlConnect(sqlStart())):
	for i in movieAndRegex: #still needs to differentiate between past and present tense SENTENCES, not just words
		PossibleTweetList = list(twitterDB.find({"text":{"$regex":i[1]}}).limit(50))
		for tweet in PossibleTweetList:
			if regexFilter(tweet):
				spoil(tweet,i,sqlc)
				
movies =[
		"John Wick",
		"The Maze Runner",
		"Ouija","Annabelle",
		"Big Hero 6",
		"Interstellar",
		"Nightcrawler",
		"Fury",
		"Gone Girl",
		"The Book of Life",
		"The Judge",
		"Birdman",
		"Horns",
		]

query(genMoviesRegexTuple(movies,genRegex(movies)))
					