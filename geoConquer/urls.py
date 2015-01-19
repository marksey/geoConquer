from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geoConquer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/$', 'helloWorld.views.dashboard', name='dashboard'),
    url(r'^json_local_tweets/$', 'twitter_api.twitter_api.json_local_tweets', name='json_local_tweets'),
)
