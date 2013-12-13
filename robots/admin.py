from django.contrib import admin
from robots.models import Robot, Match, Tourney

# Register your models here.
admin.site.register(Robot)
admin.site.register(Match)
admin.site.register(Tourney)