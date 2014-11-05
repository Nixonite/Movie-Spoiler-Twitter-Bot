from nltk.stem.lancaster import LancasterStemmer
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

movies =["Ouija", "Interstellar","John Wick","Gone Girl"]
movieRegex = []
for i in movies:
	movieRegex.append(makeRegex(i))

st = LancasterStemmer()

for i in movieRegex: #still needs to differentiate between past and present tense SENTENCES, not just words
	PossibleTweetList = list(twitterDB.find({"text":{"$regex":i}}).limit(20))
	for tweet in PossibleTweetList:
		if ("watched" in tweet['text']) or ("saw" in tweet['text']):
			break;
		tweetWords = tweet['text'].split()
		for w in tweetWords:
			stemmed = st.stem(w)
			if stemmed == "see" or stemmed == "watch" or stemmed == "catch":
				print "Yay",tweet
				break;