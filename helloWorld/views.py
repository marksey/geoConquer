from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from twython import Twython
from twitter import Twitter, OAuth, TwitterHTTPError
import twitter, json, simplejson

# Create your views here.


def login(request):

	return render_to_response("login.html")

def dashboard(request):

	oauth_verifier = request.GET['oauth_verifier']
	APP_KEY = settings.CONSUMER_KEY
	APP_SECRET = settings.CONSUMER_SECRET

	OAUTH_TOKEN = request.session['OAUTH_TOKEN']

	OAUTH_TOKEN_SECRET = request.session['OAUTH_TOKEN_SECRET']

	twitter = Twython(APP_KEY, APP_SECRET,
	OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	final_step = twitter.get_authorized_tokens(oauth_verifier)

	OAUTH_TOKEN = final_step['oauth_token']
	OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']


	twitter = Twython(APP_KEY, APP_SECRET,
	OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	TWITTER_HANDLE = twitter.verify_credentials()['screen_name']

	request.session['OAUTH_TOKEN'] = OAUTH_TOKEN
	request.session['OAUTH_TOKEN_SECRET'] = OAUTH_TOKEN_SECRET
	request.session['APP_KEY'] = APP_KEY
	request.session['APP_SECRET'] = APP_SECRET
	request.session['TWITTER_HANDLE'] = TWITTER_HANDLE
	

	profile_pic_url = twitter.show_user(screen_name=TWITTER_HANDLE)['profile_image_url_https']

	print(profile_pic_url)

	return render_to_response("dashboard.html", {"twitter_handle": TWITTER_HANDLE, "profile_pic_url": profile_pic_url})

def twitter_login(request):

	APP_KEY = settings.CONSUMER_KEY
	APP_SECRET = settings.CONSUMER_SECRET

	twitter = Twython(APP_KEY, APP_SECRET)
	auth = twitter.get_authentication_tokens(callback_url='http://127.0.0.1:8000/dashboard')

	OAUTH_TOKEN = auth['oauth_token']
	OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

	request.session['OAUTH_TOKEN'] = OAUTH_TOKEN
	request.session['OAUTH_TOKEN_SECRET'] = OAUTH_TOKEN_SECRET

	#request.session['OAUTH_TOKEN'] = '2798500298-4bN1tVRidLK8wlAt4QshEnQX5ep6NLb5FfkQE36'
	#request.session['OAUTH_TOKEN_SECRET'] = '6nfZGw7sjTF5AXFfCQCxxyLnkSES7WWZWLvfkPC2ooyrQ'

	print("APP_KEY = '%s'" % (APP_KEY))
	print("APP_SECRET = '%s'" % (APP_SECRET))
	print("OAUTH_TOKEN = '%s'" % (OAUTH_TOKEN))
	print("OAUTH_TOKEN_SECRET = '%s'" % (OAUTH_TOKEN_SECRET))

	return HttpResponseRedirect(auth['auth_url'])

def twitter_logout(request):
    
    try:
        request.session.flush()
        print("logged out")
    except Exception as e:
        print("Logout error: %s" % (str(e)))
        
    return HttpResponseRedirect("/login")