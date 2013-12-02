from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from robots.models import Robot, Match
from robots.challenge import play_match, calculate_elo_rank
from django.shortcuts import render

# Create your views here.
class RobotListView(generic.ListView):
	# model = Robot
	queryset = Robot.objects.order_by("-elo_score")

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
	
def reset_scores(request):
	for bot in Robot.objects.all():
		bot.elo_score = 1200
		bot.save()
	return HttpResponseRedirect(reverse('robots:index'))

def run_tournament(request):
	matches = []
	for challenger in Robot.objects.all():
		for defender in Robot.objects.exclude(pk=challenger.id):
			exc, match = play_match(challenger, defender)
			if match is None:
				return HttpResponse("Tournament failed: {0}".format(exc))
			else:
				challenger.elo_score, defender.elo_score = calculate_elo_rank(challenger.elo_score, defender.elo_score, match.challenger_score > match.defender_score)
				challenger.save()
				defender.save()
				matches.append(match.id)
	request.session['matches'] = matches
	return HttpResponseRedirect(reverse('robots:tourney_results'))
	
def tourney_results(request):
	matches = request.session['matches']
	return render(request, 'robots/tourney_results.html', {
		'match_list': Match.objects.filter(pk__in=matches)												
	})
