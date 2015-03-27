from twitter import Twitter, OAuth, TwitterHTTPError
import time
import datetime
from dateutil.parser import parse as parse_date


OAUTH_TOKEN = '2522040691-NCx1MQQUWKcFrPfNYpJGnAhkaEnXOHJG8PjCMlo'	#LA
OAUTH_SECRET = 'YtIkH5vqkwKgLIqgihetiIqMfUn2VlIr1OzA2xfJJJOZF'		#LA
#OAUTH_TOKEN = '3072249044-pgwdBP6lhOllYTXCDzegCrqYAbbZE0Ub1oL6JSp'  #SF
#OAUTH_SECRET = 'ueVi9saV3GA1IRSSav4Cm2CleFSnXKzhBJ2Ccib6A4uSX'		#SF
#OAUTH_TOKEN = '3075870140-bizNRXcdHD6Y6agtwB03hxh2nB6dHPnfw7HuGjg'	#NY
#OAUTH_SECRET = 'VFmcslbtX47M4wRbNiunTZAL60bozLQCmOgFMLbtIw5L5Y'		#NY
CONSUMER_KEY = 'xG5V6MDF4HCdKkh12AOoWbEcQ'	
CONSUMER_SECRET = 'Fdekjt8rRNFegU3069LEaGNKEV44TqNheF970Tek6sZGxDdguj'

italian_keywords = ['pizza', 'pasta', 'spaghetti', 'panini']

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
    CONSUMER_KEY, CONSUMER_SECRET))


tweet_results_file = 'sent_coupons_LA_C.txt'

msg = "Don't miss Disko Nekro! Watch this video http://pi.vu/6B3H & 'ReTweet' and we'll get you in free! #dragonfly"


LA_coords = '34.052234,-118.243685'
SF_coords = '37.773685,-122.421034'
NY_coords = '40.790278, -73.959722'


def tweet_older_than(tweet, mins_ago):
    
    tweet_date = None
    
    try:    
        tweet_date = parse_date(tweet['created_at']).replace(tzinfo=None) #Remove timezone info
        n_mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=mins_ago)
    except Exception, e:
        print("Couldnt process date because of %s" % str(e))
        
    if tweet_date < n_mins_ago: #Tweet older than
        return True
    else:
        return False



def sendTweet(t, user, msg, *positional_parameters, **keyword_parameters):

	#Optional parameters: img, in_reply_to_status_id

	status = "@" + user + " " + msg
	params = {"status" : status}

	print "Status: " + status

	if 'img' in keyword_parameters:

		with open(keyword_parameters['img'], "rb") as imagefile:

			params["media[]"] = imagefile.read()	#Add an image to the tweet

			if 'in_reply_to_status_id' in keyword_parameters:

				 params["in_reply_to_status_id"] = keyword_parameters['in_reply_to_status_id'] #Replying to specific status

		try:
			t.statuses.update_with_media(**params)
		except Exception as e:
			print "Couldn't send: " + str(e)



	else:

		if 'in_reply_to_status_id' in keyword_parameters:

			t.statuses.update(status=params['status'], in_reply_to_status_id=keyword_parameters['in_reply_to_status_id'])

		else:
			t.statuses.update(status=params['status'])


def get_already_sent():

	with open("dont_send.txt", "r") as ins:
		alreadySent = []

		for line in ins:
			alreadySent.append(line.split(',')[-1].rstrip())

	return alreadySent

def geo_search_tweets(t, q, coords, radius):
    """
        Returns a list of tweets matching a certain phrase and location
    """

    return t.search.tweets(q=q, geocode='%s,%dkm' % (coords, radius), result_type='mixed', count=100)

def send_tweets_to_keywords(keywords, max_tweets):

	f = open(tweet_results_file, 'w')

	#alreadySent = getAlreadySent()

	status_id_to_user_name = {}
	status_id_to_keyword = {}
	user_name_to_id = {}
	num_tweets_sent = 0


	for food_keyword in keywords:
			
		
		result = geo_search_tweets(t=t, q=food_keyword, coords=LA_coords, radius=30)

		for tweet in result['statuses']:

			if num_tweets_sent == max_tweets:
				break

			if not tweet_older_than(tweet, 120):
				print "Tweet is fresher than 120 minutes: @" + user_name + " : " + food_keyword

			user_name = tweet['user']['screen_name']
			user_id = tweet['user']['id']
			status_id = str(tweet['id']).encode("utf-8")

			try:
				#sendTweet(t, user=user_name, msg=msg, img=img, in_reply_to_status_id=status_id)
				num_tweets_sent += 1
				print str(num_tweets_sent) + " " + food_keyword + "\n"
				f.write("Sent coupon: " + food_keyword + "," + user_name + "," + str(user_id) + "," + status_id + '\n') # python will convert \n to os.linesep
			except Exception as e:
				print(e)
				f.write("Error sending coupon to " + user_name + "\n")
	


	f.close() # you can omit in most cases as the destructor will call if


def send_tweets_to_followers(user_name, msg, max_coupons, *positional_parameters, **keyword_parameters):

	file_name = 'sent_to_' + user_name + '_followers.txt'

	f = open(file_name, 'w')

	#alreadySent = getAlreadySent()

	num_tweets_sent = 0
	users_followers = t.followers.ids(screen_name=user_name)["ids"]

	for user_id in users_followers:

		try:
			user_name = t.users.lookup(user_id=user_id)[0]['screen_name']
		except:
			continue

		print "USER_ID: " + str(user_id)

		if last_tweet_older_than(t, user_id, hours_ago=200):
			print("%s hasn't even tweeted in 200 hours!\n" % (user_name))
			continue

		if num_tweets_sent == max_coupons:
				break

		try:
			if 'img' in keyword_parameters:
				sendTweet(t, user=user_name, msg=msg, img=keyword_parameters['img'])
				#pass
			else:
				sendTweet(t, user=user_name, msg=msg)
				#pass
			num_tweets_sent += 1
			f.write("Sent tweet to " +  user_name + ',' + str(user_id) + '\n') # python will convert \n to os.linesep
		except Exception as e:
			print(e)
			f.write("Error sending coupon to " + user_name + "\n")
	
	f.close() # you can omit in most cases as the destructor will call if


def get_totals(analysis):

	total_favorites = 0
	total_retweets = 0
	total_coupons = 0


	for keyword in analysis:
		total_favorites += analysis[keyword]['total_favorites']
		total_retweets += analysis[keyword]['total_retweets']
		total_coupons += analysis[keyword]['coupons_sent']

	return {
		'total_favorites' : total_favorites,
		'total_retweets'  : total_retweets,
		'total_coupons'   : total_coupons
	}


def analyze_tweets(all_tweets):

	f = open(coupon_results_file, 'w')

	analysis = {}

	for tweet in all_tweets:
		#check if this was a coupon tweet
			if msg in tweet['text']:
				in_reply_to_status_id = tweet['in_reply_to_status_id']
				try:
					in_reply_to_status = t.statuses.oembed(_id=in_reply_to_status_id)
					time.sleep(5)
					for food_keyword in food_keywords:
						if food_keyword in in_reply_to_status['html']:
							#line = "Keyword: %s Consideration: %s CTA: %s has %d favorites and %d retweets in reply to status id: %s\n" % (food_keyword, consideration, cta, tweet['favorite_count'], tweet['retweet_count'], in_reply_to_status_id)
							if food_keyword in analysis:
									analysis[food_keyword] = {
									'total_favorites' :  analysis[food_keyword]['total_favorites'] + tweet['favorite_count'], 
									'total_retweets' : analysis[food_keyword]['total_retweets'] + tweet['retweet_count'],
									'coupons_sent' : analysis[food_keyword]['coupons_sent'] + 1
									}
									#f.write(line)
							else:
								analysis[food_keyword] = {'total_favorites'  : 0, 'total_retweets' : 0, 'coupons_sent' : 0}
							break
				except Exception as e:
					print "error"
					print e

	f.close()

	return analysis

def delete_coupon_tweets(all_tweets):

	num_deleted = 0

	for tweet in all_tweets:
		if "50% OFF" in tweet['text']:
			try:
				num_deleted += 1
				t.statuses.destroy(id=tweet['id'])
				print str(num_deleted) + ": Deleted "  + tweet['text'] + "\n"
			except Exception as e:
				print str(e)
				print tweet['text']
				print "Couldn't destroy status: " + str(tweet['id'])



def get_all_tweets(screen_name):


	all_tweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count at one time)
	new_tweets = t.statuses.user_timeline(screen_name=screen_name,count=200)

	#save the most recent tweets
	all_tweets.extend(new_tweets)


	#save the id of the oldest tweet less one
	oldest = all_tweets[-1]["id"] - 1

	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsequent requests use the max_id param to prevent duplicates
		new_tweets = t.statuses.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		all_tweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = all_tweets[-1]["id"] - 1
		
		print "...%s tweets downloaded so far" % (len(all_tweets))

	return all_tweets


def last_tweet_older_than(t, user_id, hours_ago):
    
    try:
    	last_tweet = t.statuses.user_timeline(user_id=user_id)[0]
    except:
    	return False

    last_tweet_date = None
    n_weeks_ago = 0
    
    try:    
        last_tweet_date = parse_date(last_tweet['created_at']).replace(tzinfo=None) #Remove timezone info
        n_weeks_ago = datetime.datetime.now() - datetime.timedelta(hours=hours_ago)
    except Exception, e:
        print("Couldnt process date because of %s" % str(e))
        
    
    if last_tweet_date < n_weeks_ago: #Tweet older than
        return True
    else:
        return False


all_tweets = get_all_tweets('zumespot')
#analysis = analyze_tweets(all_tweets)




