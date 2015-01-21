from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geoConquer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'helloWorld.views.login', name='login'),
    url(r'^dashboard/$', 'helloWorld.views.dashboard', name='dashboard'),
    url(r'^twitter_login/$', 'helloWorld.views.twitter_login', name='twitter_login'),
    url(r'^twitter_logout/$', 'helloWorld.views.twitter_logout', name='twitter_logout'),
    url(r'^json_local_tweets/$', 'twitter_api.twitter_api.json_local_tweets', name='json_local_tweets'),
    url(r'^favorite_tweet/$', 'twitter_api.twitter_api.favorite_tweet', name='favorite_tweet'),
    url(r'^login/$', 'helloworld.views.login', name='login'),

)
