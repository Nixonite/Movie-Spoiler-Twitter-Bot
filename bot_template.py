#taken from https://github.com/cem3394/csun

import os
import sys
import time
import json
import twitter

from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file , read_token_file
from twitter.oauth_dance import oauth_dance
from urllib2 import URLError
from httplib import BadStatusLine

sys.path.append("/Users/nixonite/Documents/Code/Github/MovieSpoilerBot") 
#put the directory of the keys 1 level above the project directory to hide from accidental commits
import moviespoilerbotkeys as msbk

#import any other natual processing libs


# go to http://twitter.com/apps/new to create an app and get values
# for these credentials that you'll need to provide in place of these
# empty string values that are defined as placeholders.
    
def oauth_login():
    auth = twitter.oauth.OAuth(msbk.OAUTH_TOKEN, msbk.OAUTH_TOKEN_SECRET,
                               msbk.CONSUMER_KEY, msbk.CONSUMER_SECRET)
    
    twitter_api = Twitter(auth=auth)
    return twitter_api

# nested helper function that handles common HTTPErrors. Return an updated
# value for wait_period if the problem is a 500 level error. Block until the
# rate limit is reset if it's a rate limiting issue (429 error). Returns None
# for 401 and 404 errors, which requires special handling by the caller.
    
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
    
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
        if wait_period > 3600: # Seconds
            print >> sys.stderr, 'Too many retries. Quitting.'
            raise e
    
        # See https://dev.twitter.com/docs/error-codes-responses for common codes
        if e.e.code == 401:
            print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
            return None
        elif e.e.code == 404:
            print >> sys.stderr, 'Encountered 404 Error (Not Found)'
            return None
        elif e.e.code == 429: 
            print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
            if sleep_when_rate_limited:
                print >> sys.stderr, "Retrying in 15 minutes...ZzZ..."
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print >> sys.stderr, '...ZzZ...Awake now and trying again.'
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' % \
                (e.e.code, wait_period)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e
    # End of nested helper function
    
    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError, e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print >> sys.stderr, "URLError encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise
        except BadStatusLine, e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print >> sys.stderr, "BadStatusLine encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise
                

# all of your project code can be wrapped inside of this function
# right now response just parrots the message back at the sender

def response(message):
	return message


if __name__ == "__main__":

	bot = oauth_login()
	bot_name = '@MovieSpoilerBot' #put your actual bot's name here
	
	#main loop. Just keep searching anyone talking to us
	while True:
		try:
			mentions = make_twitter_request(bot.statuses.mentions_timeline)
			
			last_id = -1
			status = make_twitter_request(bot.statuses.user_timeline)
			if len(status) > 0:
				last_id = status[-1]['in_reply_to_status_id']

			if not mentions:
				print "No one talking to us now...", time.ctime()

			for mention in mentions:
				if mention['id'] != last_id:
					message = mention['text'].replace(bot_name, '')
					speaker = mention['user']['screen_name']
					id = mention['id']
					speaker_id = str(mention['id'])

					print "[+] " + speaker + " is saying " + message
					reply = '@%s %s' % (speaker, response(message)) 
					print "[+] Replying " , reply
					bot.statuses.update(status=reply,in_reply_to_status_id=id)
			
			sleep_int = 5 #downtime interval in seconds
			print "Sleeping...\n"
			time.sleep(sleep_int)
			
		except KeyboardInterrupt:
			print"[!] Cleaning up. Last speaker_id was ", speaker_id
			sys.exit()