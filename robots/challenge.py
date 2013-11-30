from robots.models import Match
import subprocess
from django.utils import timezone
import base64


def play_match(challenger, defender):
    match = Match()
    match.challenger = challenger
    match.defender = defender

    bot1 = challenger.path.path
    bot2 = defender.path.path

    result = subprocess.check_output(['python', 'match.py', '/home/mark/projects/rg/botLeague/media/bot_code/BasicRobot.py', '/home/mark/projects/rg/botLeague/media/bot_code/SpawnGuard.py'], cwd='/home/mark/projects/rg/rgkit')
    lines = result.split('\n')

    history = lines[0]
    scores = eval(lines[1])

    match.game_play = lines[0].replace("'", '"').replace("(", "[").replace(")", "]")
    match.challenger_score = scores[0]
    match.defender_score = scores[1]
    match.match_date = timezone.now()
    match.save()

    print match
    return match