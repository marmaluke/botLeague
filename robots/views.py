from django.shortcuts import render
from django.views import generic
from robots.models import Robot

# Create your views here.
class RobotListView(generic.ListView):
	model = Robot

class RobotDetailView(generic.DetailView):
	model = Robot
