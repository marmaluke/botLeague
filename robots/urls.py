from django.conf.urls import patterns, include, url
from robots.views import RobotListView, RobotDetailView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', RobotListView.as_view(), name='index'),
    url(r'(?P<pk>\d+)/$', RobotDetailView.as_view, name='detail')
)