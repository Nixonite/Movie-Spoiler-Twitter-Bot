movies =['The Terminator', 'The Lion King', 'Princess Mononoke', 'Twilight', 'Frozen', 'Dracula', 'Guardians of the Galaxy']


def makeRegex(movie):
	regex = ""
	for i in movie:
		if i == " ":
			regex+= "(\\s)?"
		else:
			regex+= "["+i.lower() + i.upper() + "]"
	return regex
	
	
movieRegex = []
for i in movies:
	movieRegex.append(makeRegex(i))

import nltk
stemmer = nltk.WordNetLemmatizer()
tweet = "basldfjasdf oij sdfoij asdf oi asdfoj asf"
lemmas = []
tweetWords = tweet.split()
for w in tweetWords:
	lemmas.append(stemmer.lemmatize(w))

for i in lemmas:
	if i == "see" or i == "watch" or i == "catch":
		return "Yay"
		break;

'''import pymongo

conn = pymongo.MongoClient()

db = conn.twitter

[ tweet.find_one({'text':{'$regex':movieRegex[i]}})['text'] for i in moviesRegex]'''