from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from robots.models import Robot, Match
from robots.challenge import play_match

# Create your views here.
class RobotListView(generic.ListView):
	#model = Robot
	queryset = Robot.objects.all()

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
	(exc, match) = play_match(challenger, defender)
	if exc is None:
		return HttpResponseRedirect(reverse('robots:match', args=(match.id,)))
	else:
		return HttpResponse("Game failed: {0}".format(exc))
