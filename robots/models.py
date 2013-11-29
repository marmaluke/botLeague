from django.db import models

# Create your models here.
class Robot(models.Model):
	name = models.CharField(max_length=200)
	elo_score = models.IntegerField(default=1200)
	path = models.FileField(upload_to='bot_code')
	owner = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class Match(models.Model):
	challenger = models.ForeignKey(Robot, related_name='as_challenger')
	defender = models.ForeignKey(Robot, related_name='as_defender')
	challenger_score = models.IntegerField()
	defender_score = models.IntegerField()
	match_date = models.DateTimeField()
	game_play = models.TextField()

	def __unicode__(self):
		return str(self.challenger) + " vs " + str(self.defender)