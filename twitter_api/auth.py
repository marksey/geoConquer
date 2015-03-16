from twitter import Twitter, OAuth, TwitterHTTPError
import time
from dateutil.parser import parse as parse_date


#OAUTH_TOKEN = '2522040691-NCx1MQQUWKcFrPfNYpJGnAhkaEnXOHJG8PjCMlo'
#OAUTH_SECRET = 'YtIkH5vqkwKgLIqgihetiIqMfUn2VlIr1OzA2xfJJJOZF'
OAUTH_TOKEN = '3065990437-cyEE91tA7CVGmhJYqM5i3Ohe8Y6oZS1zdNzg6Rh'
OAUTH_SECRET = 'BoVgAepVumBoOBMYkPwk2jCtdyW8rMwZE337RSxIZJsX4'
CONSUMER_KEY = 'xG5V6MDF4HCdKkh12AOoWbEcQ'
CONSUMER_SECRET = 'Fdekjt8rRNFegU3069LEaGNKEV44TqNheF970Tek6sZGxDdguj'

food_keyword_count = {}
food_keywords = ['food','foodporn', 'foodie', 'foodgasm', 'nom', 'nomnomnom', 'foodpicsbruh', 'foodbaby', 'yummy', 'hungry', 'delicious', 'cooking', 'instafood', 'recipes', 'pizza', 'dinner', 'yum', 'beer', 'pasta', 'dessert', 'foods', 'desserts', 'chocolate', 'fooddiary', 'feast', 'feastday', 'churros', 'cookies', 'doughnuts', 'sweettooth' ,'icecream', 'sweet' , 'breakfast', 'lunch' ,'chocaholic', 'strawberries' ,'organic', 'fries', 'burgers', 'foodcoma', 'snack', 'vegetarian', 'wine', 'ipa' 'draft', 'beergasm', 'beeroftheday', 'mmmbeer', 'craftbeerporn', 'brewery', 'lowbrau', 'homebrew', 'beerchat', 'drunk', 'nowdrinking', 'craftbeer', 'sacbeer', 'bored', 'donut', 'innout', 'coffee', 'icecream', 'ice cream', 'starbucks', 'mcdonald', 'kfc', 'taco bell', 'chipotle']


t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
    CONSUMER_KEY, CONSUMER_SECRET))

cta = 'ReTweet in the next 10 min'
consideration = 'Not 2 late 4 brunch!'

#status_id = '574286236103262208'
img = 'blizz.jpg'
#user = "threadsforgents"
msg = "How about a tasty treat? Follow Us in the next 10 min & get 40% OFF @Blizzyogurt"

LA_coords = '34.052234,-118.243685'


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

def replytoTweet(t, img, user, msg, status_id):


	status = "@" + user + " " + msg

	with open(img, "rb") as imagefile:	#img is a relative locationf

		params = {

		 	"media[]": imagefile.read(), 
		 	"status": status, 
		 	"in_reply_to_status_id" : status_id
		}

	t.statuses.update_with_media(**params)

def getAlreadySent():

	with open("dont_send2.txt", "r") as ins:
		alreadySent = []

		for line in ins:
			alreadySent.append(line.split(',')[-1].rstrip())

	return alreadySent

def geo_search_tweets(t, q, coords, radius):
    """
        Returns a list of tweets matching a certain phrase and location
    """

    return t.search.tweets(q=q, geocode='%s,%dkm' % (coords, radius), result_type='mixed', count=100)

def get_local_tweets(keywords):

	f = open('blizz.txt','w')

	#alreadySent = getAlreadySent()

	status_id_to_user_name = {}
	status_id_to_keyword = {}
	user_name_to_id = {}
	num_coupons_sent = 0



	for food_keyword in keywords:
			
		print "Food Keyword: "
		print food_keyword
		print "------------------\n"

		result = geo_search_tweets(t=t, q=food_keyword, coords=LA_coords, radius=30)

		for tweet in result['statuses']:

			#if tweet_older_than(tweet, 120):
			#	print "Tweet is older than 120 minutes"

			user_name = tweet['user']['screen_name']
			user_id = tweet['user']['id']
			status_id = str(tweet['id']).encode("utf-8")

			status_id_to_user_name[status_id] = user_name
			user_name_to_id[user_name] = user_id
			status_id_to_keyword[status_id] = food_keyword


	for status_id, user_name in status_id_to_user_name.items():


		user_id = user_name_to_id[user_name]
		food_keyword = status_id_to_keyword[status_id]
		if food_keyword in food_keyword_count:
			food_keyword_count[food_keyword] += 1
		else:
			food_keyword_count[food_keyword] = 0

		try:
			replytoTweet(t, img, user_name, msg, status_id)
			num_coupons_sent += 1
			f.write("Sent coupon: " + food_keyword + "," + user_name + "," + str(user_id) + "," + status_id + '\n') # python will convert \n to os.linesep
		except Exception as e:
			print(e)
			f.write("Error sending coupon to " + user_name + "\n")
		#else:
		#	print "Already sent to: " + user_name + "\n"


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

	f = open('coupon_analysis.txt','w')

	analysis = {}


	for tweet in all_tweets:
		#check all cta's 
		#check if this was a coupon tweet
		if consideration in tweet['text']:
			print tweet['text']
			if cta in tweet['text']:
				in_reply_to_status_id = tweet['in_reply_to_status_id']
				try:
					in_reply_to_status = t.statuses.oembed(_id=in_reply_to_status_id)
					time.sleep(5)
					for food_keyword in food_keywords:
						if food_keyword in in_reply_to_status['html']:
							line = "Keyword: %s Consideration: %s CTA: %s has %d favorites and %d retweets in reply to status id: %s\n" % (food_keyword, consideration, cta, tweet['favorite_count'], tweet['retweet_count'], in_reply_to_status_id)
							if food_keyword in analysis:
									print food_keyword + " top"
									analysis[food_keyword] = {
									'total_favorites' :  analysis[food_keyword]['total_favorites'] + tweet['favorite_count'], 
									'total_retweets' : analysis[food_keyword]['total_retweets'] + tweet['retweet_count'],
									'coupons_sent' : analysis[food_keyword]['coupons_sent'] + 1
									}
									#f.write(line)
							else:
								print food_keyword + " bottom"
								analysis[food_keyword] = {'total_favorites'  : 0, 'total_retweets' : 0, 'coupons_sent' : 0}
							break
				except Exception as e:
					print "error"
					print e

	f.close()

	return analysis

def delete_coupon_tweets(all_tweets):

	f = open('deleted_coupons.txt', 'w')

	for tweet in all_tweets:
		if "% off" in tweet['text']:
			try:
				print "Deleted "  + tweet['text'] + "\n"
				#t.destroy_status(tweet['id'])
				#f.write("Deleted " + tweet['text'])
			except Exception as e:
				print str(e)
				print "Couldn't destroy status: " + tweet['id'] 

	f.close()


def get_all_tweets(screen_name):


	all_tweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
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

all_tweets = get_all_tweets('zumespot')
analysis = analyze_tweets(all_tweets)





