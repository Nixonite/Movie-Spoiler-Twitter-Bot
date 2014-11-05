import nltk
import pymongo
import re


def makeRegex(movie):
	regex = ""
	for i in movie:
		if i == " ":
			regex+= "(\\s)?"
		else:
			regex+= "["+i.lower() + i.upper() + "]"
	return regex

conn = pymongo.MongoClient()

db = conn.twitter

twitterDB = db.lines

movies =["Twilight", "Frozen", "Dracula", "Guardians of the Galaxy"]
movieRegex = []
for i in movies:
	movieRegex.append(makeRegex(i))


for i in moviesRegex:
	PossibleTweetList = list(twitterDB.find({"text":{"$regex":i}})["text"].limit(20))
	for tweet in PossibleTweetList:
		stemmer = nltk.WordNetLemmatizer()
		lemmas = []
		tweetWords = tweet.split()
		for w in tweetWords:
			lemmas.append(stemmer.lemmatize(w))

		for i in lemmas:
			if i == "see" or i == "watch" or i == "catch":
				print "Yay",lemmas[lemmas.index(i)]
				break;






