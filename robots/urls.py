from django.conf.urls import patterns, url
from robots import views

urlpatterns = patterns('',
    # Examples:
    url(r'bots/$', views.RobotListView.as_view(), name='index'),
    url(r'bots/(?P<pk>\d+)/$', views.RobotDetailView.as_view(), name='detail'),
    url(r'bots/(?P<pk>\d+)/update/$', views.RobotUpdateView.as_view(), name='update'),
    url(r'bots/(?P<pk>\d+)/delete/$', views.RobotDeleteView.as_view(), name='delete'),
    url(r'bots/add/$', views.RobotCreateView.as_view(), name='add'),
    url(r'matches/(?P<pk>\d+)/$', views.MatchDetailView.as_view(), name='match'),
    url(r'tournaments/$', views.TourneyListView.as_view(), name='tourney_list'),
    url(r'tournaments/(?P<pk>\d+)/$', views.TourneyDetailView.as_view(), name='tourney'),
    url(r'bots/(?P<pk>\d+)/challenge/$', views.challenge, name='challenge'),
)