from django.db import models
from django.core.urlresolvers import reverse

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

class Match(models.Model):
    challenger = models.ForeignKey(Robot, related_name='as_challenger')
    defender = models.ForeignKey(Robot, related_name='as_defender')
    challenger_score = models.IntegerField()
    defender_score = models.IntegerField()
    match_date = models.DateTimeField()
    game_play = models.TextField()
    game_play.allow_tags = True

    def get_winner(self):
        if self.challenger_score > self.defender_score:
            return self.challenger
        elif self.challenger_score < self.defender_score:
            return self.defender
        else:
            return None

    def __unicode__(self):
        return "{0} vs {1}".format(self.challenger, self.defender)