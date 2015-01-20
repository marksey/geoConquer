                                                                                                                                                                       # -*- coding: utf-8 -*-
"""
Copyright 2014 Randal S. Olson

This file is part of the Twitter Follow Bot library.

The Twitter Follow Bot library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

The Twitter Follow Bot library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with the Twitter
Follow Bot library. If not, see http://www.gnu.org/licenses/.
"""

from sets import Set
import time
from dateutil.parser import parse as parse_date
import datetime
from twitter import Twitter, OAuth, TwitterHTTPError
from django.http import HttpResponse
from django.conf import settings
import json, simplejson


food_hashtags = ['food','foodporn', 'foodie', 'foodgasm', 'nom', 'nomnomnom', 'foodpicsbruh', 'foodbaby', 'yummy', 'hungry', 'delicious', 'cooking', 'instafood', 'recipes', 'pizza', 'dinner', 'yum', 'beer', 'pasta', 'dessert', 'foods', 'desserts', 'chocolate', 'fooddiary', 'feast', 'feastday', 'churros', 'cookies', 'doughnuts', 'sweettooth' ,'icecream', 'sweet' , 'breakfast', 'lunch' ,'chocaholic', 'strawberries' ,'organic', 'fries', 'burgers', 'foodcoma', 'snack', 'vegetarian', 'wine', 'ipa' 'draft', 'beergasm', 'beeroftheday', 'mmmbeer', 'craftbeerporn', 'brewery', 'lowbrau', 'homebrew', 'beerchat', 'drunk', 'nowdrinking', 'craftbeer', 'sacbeer']

clothes_hashtags = ['bowtie', 'bow tie', 'pocket square', 'dapper', 'style', 'shoes', 'watch', 'suit', 'tie', 'ootd', 'fashion', 'ootd', 'mensfashion', 'sneakers', 'shoes', 'selfie', 'beautiful', 'cute', 'chanel', 'travel']

niners_hashtags = ['Niners', 'NFL', 'QuestForSix', 'NinerNation', '49ers', 'NinerGang', 'football', 'kaepernick', 'crabtree', 'aldon smith', 'frank gore', 'vernon davis']

niners_hashtags2 = ['#Niners', '#NFL', '#QuestForSix', '#NinerNation', '#49ers', '#NinerGang']

lat_long = {
				'SF': '37.787711,-122.406610',
				'1WESTSTREET' : '40.705349,-74.016063',
				'SAC': '38.581572,-121.4944',
				'NYC': '40.756567,-73.985410',
				'Red Rabbit': '38.581572, -121.494400'
		   }


def favorite_tweet(request):

	tweet_id = request.GET.get('tweet_id')

	t = Twitter(auth=OAuth('2972545266-aTWaptCudDu083vnmrnlBJ43zOFD6Z06ijWSoHj', 'wDHpTExvWwRoFUtDoU3Polk4On5B77Zss32JhFa78unfh', settings.CONSUMER_KEY, settings.CONSUMER_SECRET))
 
 	print("Tweet_id: %s" % (tweet_id))

	try:
		t.favorites.create(_id=tweet_id)
		return HttpResponse("SUCCESS")
	except TwitterHTTPError as e:
		print("error: %s" % (str(e)))
		return HttpResponse("FAIL")

def geo_search_tweets(t, q, coords, radius):
    """
        Returns a list of tweets matching a certain phrase and location
    """

    return t.search.tweets(q=q, geocode='%s,%dkm' % (coords, radius), result_type='mixed', count=100)



def json_local_tweets(request):


	coords = request.GET.get('coords', '')
	q = request.GET.get('q', '')
	radius = int(request.GET.get('radius', ''))

	#print("JSON LOCAL TWEETS: %s %s" % (request.session['OAUTH_TOKEN'], request.session['OAUTH_TOKEN_SECRET']))

	already_added = []

	json_tweets = []

	t = Twitter(auth=OAuth('2972545266-aTWaptCudDu083vnmrnlBJ43zOFD6Z06ijWSoHj', 'wDHpTExvWwRoFUtDoU3Polk4On5B77Zss32JhFa78unfh', settings.CONSUMER_KEY, settings.CONSUMER_SECRET))
	result = geo_search_tweets(t=t, q=q, coords=coords, radius=radius)

	favorites = t.favorites.list(screen_name='cravesac', count=10000)
	favorited_tweets = []
	for f in favorites: favorited_tweets.append(f['id_str'])


	print("#Faves: ")
	print(len(favorites))

	for tweet in result['statuses']:

		if tweet['user']['screen_name'] not in already_added:

			#Innocent until proven guilty!
			already_favorited = False
			tweet_time_stamp = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')

			now = datetime.datetime.now()

			diff = now - tweet_time_stamp

			time_since_tweet = None

			days_since_tweet = diff.total_seconds() / 60.0 / 60 / 24

			#If we can't have days > 1, then convert to hours for readability!
			if days_since_tweet >= 1:
				time_since_tweet = str(int(days_since_tweet)) + 'd ago '
			else:
				time_since_tweet = str(int(days_since_tweet * 24)) + 'h ago '

			if str(tweet['id']) in favorited_tweets:
				already_favorited = True

			json_tweet = {
							'screen_name' : tweet['user']['screen_name'],
							'tweet_text'  : tweet['text'],
							'tweet_id'	  :	str(tweet['id']).encode("utf-8"),
							'favorited'   : already_favorited,
							'profile_image_url' : tweet['user']['profile_image_url'], 
							'latitude'			: tweet['coordinates']['coordinates'][1],
							'longitude'			: tweet['coordinates']['coordinates'][0],
							'time_since_tweet'  : time_since_tweet

						 }

			json_tweets.append(json_tweet)
					 
			already_added.append(tweet['user']['screen_name'])

	return HttpResponse(json.dumps(json_tweets), content_type="application/json")








