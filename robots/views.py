from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from robots.models import Robot, Match
from robots.challenge import play_match, calculate_elo_rank
from django.shortcuts import render
import collections

# Create your views here.
class RobotListView(generic.ListView):
    queryset = Robot.objects.order_by("-elo_score")

class RobotDetailView(generic.DetailView):
    model = Robot

    def get_context_data(self, **kwargs):
        context = super(RobotDetailView, self).get_context_data(**kwargs)
        context['all_bots'] = Robot.objects.all()
        match_history = self.object.as_challenger.all() | self.object.as_defender.all()
        context['match_history'] = match_history.order_by('-match_date')
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
    Match.objects.all().delete()
    return HttpResponseRedirect(reverse('robots:index'))

def run_tournament(request):
    matches = []
    
    for challenger in Robot.objects.all():
        for defender in Robot.objects.exclude(pk=challenger.id):
            exc, match = play_match(challenger, defender)
            if match is None:
                return HttpResponse("Tournament failed: {0}".format(exc))
            else:
                matches.append(match.id)
                print "{0} played {1}, result: {2}-{3}".format(challenger.name, defender.name, match.challenger_score, match.defender_score)

    request.session['matches'] = matches
    
    return HttpResponseRedirect(reverse('robots:tourney_results'))

def _process_tourney_results(matches):
    tournament_record = collections.defaultdict(lambda:((0, 0, 0), {}))
    for match in matches:
        print "processing match: {0}".format(match)
        challenger = match.challenger
        challenger_score = match.challenger_score
        defender = match.defender
        defender_score = match.defender_score
        
        challenger.elo_score, defender.elo_score = calculate_elo_rank(challenger.elo_score, defender.elo_score, challenger_score > defender_score)
        challenger.save()
        defender.save()
        
        c_scores, c_results = tournament_record[challenger.id]
        c_results[defender.id] = match.id
        d_scores, d_results = tournament_record[defender.id]
        cw, ct, cl = c_scores
        dw, dt, dl = d_scores
        if challenger_score > defender_score:
            cw += 1
            dl += 1
        elif challenger_score < defender_score:
            dw += 1
            cl += 1
        else:
            ct += 1
            dt += 1
        tournament_record[challenger.id] = ((cw, ct, cl), c_results)
        tournament_record[defender.id] = ((dw, dt, dl), d_results)
    return tournament_record

def _tournament_score(tournament_record, bot):
    (w, t, l), _ = tournament_record[bot.id]
    return 2 * w + t

def tourney_results(request):
    tournament_record = _process_tourney_results([Match.objects.get(pk=match_id) for match_id in request.session['matches']])
    
    sorted_bots = [Robot.objects.get(pk=challenger) for challenger in tournament_record.keys()]
    sorted_bots.sort(key=lambda x: _tournament_score(tournament_record, x), reverse=True)
    
    results = []
    for challenger in sorted_bots:
        scores, matches = tournament_record[challenger.id]
        sorted_matches = []
        for defender in sorted_bots:
            try:
                sorted_matches.append(Match.objects.get(pk=matches[defender.id]))
            except KeyError:
                sorted_matches.append(None)
        results.append((challenger, scores, sorted_matches))
    
    return render(request, 'robots/tourney_results.html', {
        't_record': results,                                            
    })
