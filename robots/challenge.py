from robots.models import Match
import subprocess
from django.utils import timezone
import base64
import math

#elo rank algorithm     
def calculate_elo_rank(challenger_rank=1600, defender_rank=1600, challenger_won=True, penalize_loser=True):
    if challenger_won:
        winner_rank, loser_rank = challenger_rank, defender_rank
    else:
        winner_rank, loser_rank = defender_rank, challenger_rank
    rank_diff = winner_rank - loser_rank
    exp = (rank_diff * -1) / 400
    odds = 1 / (1 + math.pow(10, exp))
    if winner_rank < 2100:
        k = 32
    elif winner_rank >= 2100 and winner_rank < 2400:
        k = 24
    else:
        k = 16
    new_winner_rank = round(winner_rank + (k * (1 - odds)))
    if penalize_loser:
        new_rank_diff = new_winner_rank - winner_rank
        new_loser_rank = loser_rank - new_rank_diff
    else:
        new_loser_rank = loser_rank
    if new_loser_rank < 1:
        new_loser_rank = 1
    if challenger_won:
        return (new_winner_rank, new_loser_rank)
    return (new_loser_rank, new_winner_rank)

def play_match(challenger, defender):
    match = Match()
    match.challenger = challenger
    match.defender = defender

    bot1 = challenger.path.path
    bot2 = defender.path.path

    result = subprocess.check_output(['python', 'match.py', bot1, bot2],
        cwd='/home/mark/projects/rg/rgkit'
    )
    lines = result.split('\n')

    history = lines[0]
    scores = eval(lines[1])

    match.game_play = lines[0].replace("'", '"').replace("(", "[").replace(")", "]")
    match.challenger_score = scores[0]
    match.defender_score = scores[1]
    match.match_date = timezone.now()
    match.save()

    challenger.elo_score, defender.elo_score = calculate_elo_rank(challenger.elo_score, defender.elo_score, scores[0] > scores[1])
    challenger.save()
    defender.save()

    return match