from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from robots.models import Robot, Match
from robots.challenge import play_match

# Create your views here.
class RobotListView(generic.ListView):
	model = Robot

class RobotDetailView(generic.DetailView):
	model = Robot

	def get_context_data(self, **kwargs):
		context = super(RobotDetailView, self).get_context_data(**kwargs)
		context['all_bots'] = Robot.objects.all()
		return context
	
class MatchDetailView(generic.DetailView):
	model = Match

def challenge(request, pk):
	challenger = Robot.objects.get(pk=pk)
	defender = Robot.objects.get(pk=request.POST['opponent'])
	play_match(challenger, defender)
	return HttpResponse(str(challenger.name) + " challenges " + str(defender.name))
