from nltk.stem.lancaster import LancasterStemmer
import pymongo
import re
import sqlite3


def makeRegex(movie):
	regex = "(?i)"
	for i in movie:
		if i == " ":
			regex+= "(\s)?"
		else:
			regex+= i
			
	return regex

conn = pymongo.MongoClient()

db = conn.twitter

twitterDB = db.lines

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
		"Addicted"
		]

movieRegex = []
for i in movies:
	movieRegex.append(makeRegex(i))

st = LancasterStemmer()

movieAndRegex = []

for i in range(len(movies)):
	movieAndRegex.append((movies[i],movieRegex[i]))
	
SQLCONN = sqlite3.connect('moviespoilerbot.db')
c = SQLCONN.cursor()

for i in movieAndRegex: #still needs to differentiate between past and present tense SENTENCES, not just words
	PossibleTweetList = list(twitterDB.find({"text":{"$regex":i[1]}}).limit(200))
	for tweet in PossibleTweetList:
		if ("watched" in tweet['text']) or ("saw" in tweet['text']) or ("again" in tweet['text']):
			break;
		tweetWords = tweet['text'].split()
		for w in tweetWords:
			stemmed = st.stem(w)
			if stemmed == "watch":
				tablename = "table_"+i[0][0]
				c.execute("select spoiler from "+tablename+" where TITLE=:title",{"title":i[0]})
				spoiler = c.fetchone()
				print tweet['id_str'],tweet['text'],"\n","Movie:",i[0],"\t Spoiler:",spoiler,"\n\n\n"
				break;

SQLCONN.close()
				

				