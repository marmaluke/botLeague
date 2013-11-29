from django.conf.urls import patterns, url
from robots.views import RobotListView, RobotDetailView, challenge,\
    MatchDetailView

urlpatterns = patterns('',
    # Examples:
    url(r'bots/$', RobotListView.as_view(), name='index'),
    url(r'bots/(?P<pk>\d+)/$', RobotDetailView.as_view(), name='detail'),
    url(r'matches/(?P<pk>\d+)/$', MatchDetailView.as_view(), name='match'),
    url(r'bots/(?P<pk>\d+)/challenge/$', challenge, name='challenge'),
)