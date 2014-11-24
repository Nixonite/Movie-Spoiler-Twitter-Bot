import pymongo
import re
import sqlite3
import time
import twitterwrapper
from datetime import datetime

global matchedCounter
global howMuchToSearch
howMuchToSearch = 100
matchedCounter = 0

def mongoConnect():
	try:
		print "Connecting to MongoDB..."
		conn = pymongo.MongoClient()
		db = conn.twitter
		twitterDB = db.lines
		return twitterDB
	except IOError:
		print "Can't connect to either mongo or the twitter db."
		
def sqlStart():
	try:
		print "Starting SQL..."
		return sqlite3.connect('moviespoilerbot.db')
	except IOError:
		print "Can't connect to sql db called moviespoilerbot.db"

def sqlConnect(SQLCONN):
	return SQLCONN.cursor()
	
def sqlClose(SQLCONN):
	print "Closing SQL..."
	SQLCONN.close()

def noDuplicatesSetup(sqlc):
	sqlc.execute("create table if not exists Replied_Tweets (ID INTEGER PRIMARY KEY, tweetID VARCHAR(255))")
	sqlc.commit()

###############################################################

def movieToRegex(movie):#movies -> movieregex
	regex = "((^|[^\w])"
	for i in movie:
		if i == " ":
			regex+= "\s*"
		else:
			regex+= i
	regex +="($|Movie|[^\w]))"
	return regex

def moviesToRegexList(movies):#generates regex for the movies list
	movieRegex = []
	for i in movies:
		movieRegex.append(movieToRegex(i))
	return movieRegex
		
def tupleMoviesRegex(movies,movieRegex):#more convenient for later use
	print "Generating regex..."
	movieAndRegex = []
	for i in range(len(movies)):
		movieAndRegex.append((movies[i],movieRegex[i]))
	return movieAndRegex

def oneRegexToRuleThemAll(movieRegexList):
	giantMovieRegex = "(?i)"
	giantMovieRegex +=movieRegexList[0]
	for i in range(1,len(movieRegexList)):
		giantMovieRegex+="|"+movieRegexList[i]
	return giantMovieRegex
	
def rememberTheMovie(text,tupleMR):
	for i in range(len(tupleMR)):
		if re.search("(?i)"+tupleMR[i][1],text):
			return str(tupleMR[i][0])

###############################################################

def isTweetRecent(bot,str_id):
	try:
		tweetTime = bot.statuses.show(id=str_id)#mybot = oauth_login()
		tweetTime = tweetTime['created_at']#u'Thu Nov 13 21:47:43 +0000 2014'
		tweetTimeList = tweetTime.split()
		del tweetTimeList[0]
		del tweetTimeList[-2]
		tweetTime = " ".join(tweetTimeList)
		tweetTime = datetime.strptime(tweetTime,'%b %d %H:%M:%S %Y')
		presentTime = datetime.now()

		timedelta = presentTime - tweetTime
		if timedelta.days <2:
			if timedelta.seconds < 3600*24: #less than 3 hours
				print tweetTime
				return True
		return False
	except Exception:
		pass

###############################################################

def regexFilter(tweet):#trivial time
	text = tweet['text'].lower()
	if re.search("watched|saw|again|seen|watches|was|great|remember|after|seat|back\s*from|from\s*watching|while\s*watching|fantastic|amazing|cool|favo(u)?rite|good|went|were|second\s*time|produced|funny|sad|recommend|sweet|after\s*seeing|after\s*watching|ending|never\s*watch|never\s*see",text) is None:
	#the above regex excludes stuff like fantastic/great/amazing etc. because they often come in the form of a review of the film i.e. already watched it.
		if re.search("watching|gonna\s*see|gonna\s*watch|wanna\s*see|want\s*to\s*see|going\s*to\s*see|seeing|going\s*to\s*watch|wanna\s*watch|wanna\s*go\s*see|want\s*to\s*go\s*see|I\s*need\s*to\s*see|I\s*have\s*to\s*watch|I\s*need\s*to\s*watch|want\s*to\s*watch|going\s*to\s*the\s*movies|watch\s*a\s*movie|see\s*a\s*movie|watching\s*a\s*movie|at\s*the\s*movies|about\s*to\s*watch|about\s*to\s*see|I\s*need\s*to\s*watch",text):
			return True
	return False
	
###############################################################

def spoil(tweet,title,sqlc):#the act of evil
	tablename = "table_"+title[0]
	sqlc.execute("select spoiler from "+tablename+" where TITLE=:title",{"title":title})
	spoiler = sqlc.fetchone()
	print tweet['id_str'],tweet['text'],"\n","Movie:",title,"\t Spoiler:",spoiler,"\n"
	

###############################################################


def noDuplicate(id_str,sqlCURSOR):
	sqlCURSOR.execute("select tweetID from Replied_Tweets where tweetID=:tID",{"tID":id_str})
	result = sqlCURSOR.fetchone()
	if result is None:
		return True
	else: return False

def insertDuplicatesTable(id_str,sqlCURSOR,sqlCONN):
	sqlCURSOR.execute("insert into Replied_Tweets (tweetID) values (:tID)",{"tID":id_str})
	sqlCONN.commit()

###############################################################

def query(bigMovieRegex,twitterDB,sqlCURSOR,sqlCONN,bot):#maybe needs a better name since it both queries the mongodb and spoils

	global howMuchToSearch
	global matchedCounter
	
	startT = time.time()
	print "\n\n\nStarting a search in the database for ",howMuchToSearch," possible tweets..."
	PossibleTweetList = list(twitterDB.find({"text":{"$regex":bigMovieRegex}}).sort([['id_str', -1]]).limit(howMuchToSearch))# sorting by str_id is faster than _id

	print "Time it took: ",time.time()-startT
	print "Done. Now seeing if they match..."
	
	movieRegTupe = tupleMoviesRegex(movies,moviesToRegexList(movies))
	for tweet in PossibleTweetList:
		if noDuplicate(tweet['id_str'],sqlCURSOR):
			if regexFilter(tweet):
				try:
					if isTweetRecent(bot,tweet['id_str']):
						title = rememberTheMovie(tweet['text'],movieRegTupe)
						spoil(tweet,title,sqlCURSOR)
						insertDuplicatesTable(tweet['id_str'],sqlCURSOR,sqlCONN)
						matchedCounter+=1
				except Exception:
					pass
		

###############################################################

movies =[#should be moved to main.py in the future
		"The Maze Runner",
		"Ouija",
		"Annabelle",
		"Big Hero 6",
		"Interstellar"
		"Nightcrawler",
		"Fury",
		"Gone Girl",
		"The Losers",
		"The Lord of the Rings",
		"The Wolf of Wall Street",
		"The Matrix Reloaded",
		"The Machinist",
		"The Book of Life",
		"Cidade de Deus",
		"The Number 23",
		"The Limits of Control",
		"The Sixth Sense",
		"The Mothman Prophecies",
		"The Muppet Movie",
		"The Mechanic",
		"The Breakfast Club",
		"Twelve Monkeys",
		"The Maiden Heist",
		"The Next Three Days",
		"The Adjustment Bureau",
		"The Departed",
		"The Hurt Locker",
		"The Judge",
		"Birdman",
		"Under the Mountain",
		"Unbreakable",
		"Goodfellas",
		"Green Zone",
		"Gone with the Wind",
		"Good Will Hunting",
		"Gone Baby Gone",
		"Gran Torino",
		"Edge of Darkness",
		"Eternal Sunshine of the Spotless Mind",
		"Edge of Tomorrow",
		"Eragon",
		"Captain America: The First Avenger",
		"Cloudy With Chance Of Meatballs",
		"Catch 44",
		"Children of Men",
		"Cloverfield",
		"Horns"
		]
		
#general comments on the movie database:
#fix double single quotes
#fix some unicode mistakes

#turns out it's faster with more popular movies, not more movies.

###############################################################

megaRegex = oneRegexToRuleThemAll(moviesToRegexList(movies))
twitterDB=mongoConnect()
sqlCONN = sqlStart()
sqlCURSOR= sqlConnect(sqlCONN)
noDuplicatesSetup(sqlCONN)

bot = twitterwrapper.oauth_login()
bot_name = '@MovieSpoilerBot' #put your actual bot's name here

for i in range(2):
	query(megaRegex,twitterDB,sqlCURSOR,sqlCONN,bot)
	print "Total Matches: ",matchedCounter,"/",howMuchToSearch
	matchedCounter=0

#print oneRegexToRuleThemAll(moviesToRegexList(movies))


###############################################################