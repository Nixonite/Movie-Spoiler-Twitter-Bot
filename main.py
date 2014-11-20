#import import import

#main script + gui maybe?

#still requires method of checking if spoiled already
#maybe either write to file a list of IDs already replied to like in bot_template or
#write to a sqltable. Whichever is faster/easier/whatever.

'''
def isTweetRecent(idNum):
	#assuming not already replied to this idNum
	#assuming idNum is not a string
	firstTime = mybot.statuses.show(id=idNum)#mybot = oauth_login()
	firstTime = firstTime['created_at']#u'Thu Nov 13 21:47:43 +0000 2014'
	currentTime = current date and time
	
	from datetime import datetime
	convertedFirstTime = datetime.strptime(firstTime,'%a %b %d %H:%M:%S %z %Y')
	
	#doesn't work since ValueError: 'z' is a bad directive in format '%a %b %d %H:%M:%S %z %Y'
	#maybe have to manually remove the %z portion and try again with the below
	convertedFirstTime = datetime.strptime(firstTime,'%a %b %d %H:%M:%S %Y')
	#pain in the ass
	
	#subtract current time from firstTime (poorly named, it should be called tweetTime)
	#if subtraction yields less than 2-3 hours then it's good and should be spoiled immediately.
'''