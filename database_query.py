from nltk.stem.lancaster import LancasterStemmer
import pymongo
import re
import sqlite3

global matchedCounter
matchedCounter = 0

def toRegex(movie):#movies -> movieregex
	regex = "(?i)[^\w]"
	for i in movie:
		if i == " ":
			regex+= "(\s)?"
		else:
			regex+= i
	regex +="[^\w]"
	return regex

def mongoConnect():
	try:
		conn = pymongo.MongoClient()
		db = conn.twitter
		twitterDB = db.lines
		return twitterDB
	except IOError:
		print "Can't connect to either mongo or the twitter db."	

def genRegex(movies):#generates regex for the movies list
	movieRegex = []
	for i in movies:
		movieRegex.append(toRegex(i))
	return movieRegex
		
def genMoviesRegexTuple(movies,movieRegex):#more convenient for later use
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

def regexFilter(tweet):#takes out false positive tweets
	if re.search("(?i)watched|saw|again|seen|watches|was|great|after watching|fantastic|amazing|cool|favorite|good|went|were|second\stime|produced",tweet['text']) is None:
		#the above regex excludes stuff like fantastic/great/amazing etc. because they often come in the form of a review of the film i.e. already watched it.
		if re.search("(?i)watching|wanna see|want to see|wanna watch|want to watch",tweet['text']):		
			return True
	return False

def spoil(tweet,movieAndRegex,sqlc):#the act of evil
	tablename = "table_"+movieAndRegex[0][0]
	sqlc.execute("select spoiler from "+tablename+" where TITLE=:title",{"title":movieAndRegex[0]})
	spoiler = sqlc.fetchone()
	print tweet['id_str'],tweet['text'],"\n","Movie:",movieAndRegex[0],"\t Spoiler:",spoiler,"\n"

def query(movieAndRegex,twitterDB=mongoConnect(),sqlc=sqlConnect(sqlStart())):#maybe needs a better name since it both queries the mongodb and spoils
	for i in movieAndRegex:
		print "\n\n=================================================\n"
		print "Looking for ",i[0],"...\n"#movie name
		PossibleTweetList = list(twitterDB.find({"text":{"$regex":i[1]}}).sort([['_id', -1]] ).limit(10))
		print "Possible Targets: ",len(PossibleTweetList)
		
		failedMatchCounter = 0
		for tweet in PossibleTweetList:
			if regexFilter(tweet):
				spoil(tweet,i,sqlc)
				global matchedCounter
				matchedCounter+=1
			else:
				failedMatchCounter+=1
		print failedMatchCounter,"/",len(PossibleTweetList)," skipped.\n\n"
				
movies =[#should be moved to main.py in the future
		"The Maze Runner",
		"Ouija",
		"Annabelle",
		"Big Hero 6",
		"Interstellar",
		"Nightcrawler",
		"Fury",
		"Gone Girl",
		"The Book of Life",
		"Birdman",
		"Horns"
		]

query(genMoviesRegexTuple(movies,genRegex(movies)))#test
print "Total Matches: ",matchedCounter