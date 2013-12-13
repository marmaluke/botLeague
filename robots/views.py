from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from robots.models import Robot, Match, Tourney
from robots.challenge import play_match, calculate_elo_rank
import collections
from django.utils import timezone

# Create your views here.
class RobotListView(generic.ListView):
    queryset = Robot.objects.order_by("-elo_score")

    def post(self, request, *args, **kwargs):
        if 'run_tournament' in request.POST:
            return _run_tournament(request)
        elif 'reset' in request.POST:
            for bot in Robot.objects.all():
                bot.elo_score = 1200
                bot.save()
            Match.objects.all().delete()
            return HttpResponseRedirect(reverse('robots:index'))
        else:
            return HttpResponseRedirect(reverse('robots:index'))

class RobotDetailView(generic.DetailView):
    model = Robot

    def get_context_data(self, **kwargs):
        context = super(RobotDetailView, self).get_context_data(**kwargs)
        context['all_bots'] = Robot.objects.all()
        match_history = self.object.as_challenger.all() | self.object.as_defender.all()
        context['match_history'] = match_history.order_by('-match_date')
        return context

class RobotCreateView(generic.CreateView):
    model = Robot
    fields = ['name', 'path', 'owner']

class RobotUpdateView(generic.UpdateView):
    model = Robot
    fields = ['name', 'path', 'owner']

class RobotDeleteView(generic.DeleteView):
    model = Robot
    success_url = reverse_lazy('robots:index')
    
class MatchDetailView(generic.DetailView):
    model = Match
    
class TourneyListView(generic.ListView):
    queryset = Tourney.objects.order_by("-tourney_date")

def _tournament_score(tournament_record, bot):
    (w, t, _), _ = tournament_record[bot]
    return 2 * w + t
   
class TourneyDetailView(generic.DetailView):
    model = Tourney
    
    def get_context_data(self, **kwargs):
        tournament_record = self.object.get_tournament_record()
            
        sorted_bots = sorted(self.object.get_bots(), key=lambda x: _tournament_score(tournament_record, x), reverse=True)
        
        results = []
        for challenger in sorted_bots:
            scores, matches = tournament_record[challenger]
            sorted_matches = []
            for defender in sorted_bots:
                try:
                    sorted_matches.append(matches[defender])
                except KeyError:
                    sorted_matches.append(None)
            results.append((challenger, scores, sorted_matches))
        context = super(TourneyDetailView, self).get_context_data(**kwargs)
        context['t_record'] = results
        return context
    
def challenge(request, pk):
    challenger = Robot.objects.get(pk=pk)
    defender = Robot.objects.get(pk=request.POST['opponent'])
    exc, match = play_match(challenger, defender)
    if match is None:
        return HttpResponse("Game failed: {0}".format(exc))
    else:
        return HttpResponseRedirect(reverse('robots:match', args=(match.id,)))
    
def _run_tournament(request):
    tourney = Tourney()
    tourney.tourney_date = timezone.now()
    tourney.save()
    
    for challenger in Robot.objects.all():
        for defender in Robot.objects.exclude(pk=challenger.id):
            exc, match = play_match(challenger, defender)
            if match is None:
                return HttpResponse("Tournament failed: {0}".format(exc))
            else:
                match.tourney = tourney
                match.save()
                print "{0} played {1}, result: {2}-{3}".format(challenger.name, defender.name, match.challenger_score, match.defender_score)
    
    for match in tourney.match_set.all():
        new_challenger_rank, new_defender_rank = calculate_elo_rank(match.challenger.elo_score, match.defender.elo_score, match.challenger_score > match.defender_score) 
        match.challenger.elo_score = new_challenger_rank
        match.challenger.save()
        match.defender.elo_score = new_defender_rank
        match.defender.save()
        
    return HttpResponseRedirect(reverse('robots:tourney', args=(tourney.pk,)))
