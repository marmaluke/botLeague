from django.db import models
from django.core.urlresolvers import reverse
import collections

# Create your models here.
class Robot(models.Model):
    name = models.CharField(max_length=200)
    elo_score = models.IntegerField(default=1200)
    path = models.FileField(upload_to='bot_code')
    owner = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('robots:detail', args=[self.pk])

    def __unicode__(self):
        return self.name 

class Tourney(models.Model):
    tourney_date = models.DateTimeField()
    
    def get_bots(self):
        bots = set()
        for match in self.match_set.all():
            bots.add(match.challenger)
        return bots
    
    def get_winner(self):
        tournament_record = self.get_tournament_record()
        ranked = sorted(self.get_bots(), key=lambda b:2 * tournament_record[b][0][0] + tournament_record[b][0][1], reverse=True)
        if len(ranked) > 0:
            return ranked[0]
        else:
            return None
    
    def get_tournament_record(self):
        tournament_record = collections.defaultdict(lambda:((0, 0, 0), {}))
        for match in self.match_set.all():
            challenger = match.challenger
            challenger_score = match.challenger_score
            defender = match.defender
            defender_score = match.defender_score
            
            c_scores, c_results = tournament_record[challenger]
            c_results[defender] = match
            d_scores, d_results = tournament_record[defender]
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
            tournament_record[challenger] = ((cw, ct, cl), c_results)
            tournament_record[defender] = ((dw, dt, dl), d_results)
        return tournament_record
    
    def get_absolute_url(self):
        return reverse('robots:tourney', args=[self.pk])
    
    def __unicode__(self):
        return "Tourney {0}: {1}".format(self.tourney_date, self.get_bots())

class Match(models.Model):
    challenger = models.ForeignKey(Robot, related_name='as_challenger')
    defender = models.ForeignKey(Robot, related_name='as_defender')
    challenger_score = models.IntegerField()
    defender_score = models.IntegerField()
    match_date = models.DateTimeField()
    game_play = models.TextField()
    game_play.allow_tags = True
    tourney = models.ForeignKey(Tourney, null=True, on_delete=models.SET_NULL)

    def get_winner(self):
        if self.challenger_score > self.defender_score:
            return self.challenger
        elif self.challenger_score < self.defender_score:
            return self.defender
        else:
            return None

    def __unicode__(self):
        return "{0} vs {1}".format(self.challenger, self.defender)
    