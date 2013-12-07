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
    url(r'bots/(?P<pk>\d+)/challenge/$', views.challenge, name='challenge'),
    url(r'reset_scores/$', views.reset_scores, name='reset_scores'),
    url(r'tourney/$', views.run_tournament, name='run_tournament'),
    url(r'results/$', views.tourney_results, name='tourney_results'),
)