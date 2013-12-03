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
	exc, match = play_match(challenger, defender)
	if match is None:
		return HttpResponse("Game failed: {0}".format(exc))
	else:
		return HttpResponseRedirect(reverse('robots:match', args=(match.id,)))
	
def reset_scores(request):
	for bot in Robot.objects.all():
		bot.elo_score = 1200
		bot.save()
	return HttpResponseRedirect(reverse('robots:index'))

def run_tournament(request):
	matches = []
	tournament_record = dict([(bot.id, (0,0,0)) for bot in Robot.objects.all()])
	
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
				cw, cl, ct = tournament_record[challenger.id]
				dw, dl, dt = tournament_record[defender.id]
				if match.challenger_score > match.defender_score:
					cw += 1
					dl += 1
				elif match.challenger_score < match.defender_score:
					dw += 1
					cl += 1
				else:
					ct += 1
					dt += 1
				tournament_record[challenger.id] = (cw, cl, ct) 
				tournament_record[defender.id] = (dw, dl, dt) 
	request.session['matches'] = matches
	request.session['t_record'] = tournament_record
	return HttpResponseRedirect(reverse('robots:tourney_results'))
	
def tourney_results(request):
	matches = request.session['matches']
	tournament_record = request.session['t_record']
	result_list = [(Robot.objects.get(pk=bot_id), record) for (bot_id, record) in tournament_record.items()]
	result_list.sort(cmp=lambda (bot_x, bot_x_rec), (bot_y, bot_y_rec): -cmp(bot_x.elo_score, bot_y.elo_score))
	return render(request, 'robots/tourney_results.html', {
		'match_list': Match.objects.filter(pk__in=matches),
		't_record': result_list,											
	})
