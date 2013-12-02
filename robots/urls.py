from django.conf.urls import patterns, url
from robots.views import RobotListView, RobotDetailView, challenge,\
    MatchDetailView, reset_scores, tourney_results, run_tournament

urlpatterns = patterns('',
    # Examples:
    url(r'bots/$', RobotListView.as_view(), name='index'),
    url(r'bots/(?P<pk>\d+)/$', RobotDetailView.as_view(), name='detail'),
    url(r'matches/(?P<pk>\d+)/$', MatchDetailView.as_view(), name='match'),
    url(r'bots/(?P<pk>\d+)/challenge/$', challenge, name='challenge'),
    url(r'reset_scores/$', reset_scores, name='reset_scores'),
    url(r'tourney/$', run_tournament, name='run_tournament'),
    url(r'results/$', tourney_results, name='tourney_results'),
)