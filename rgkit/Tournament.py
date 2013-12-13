import subprocess
import string
import os
import random
import math
import re

PLAYER_A = 1
PLAYER_B = 2

#number of rounds to play
number_of_matches=1

#elo rank algorithm     
def calculate_elo_rank(player_a_rank=1600, player_b_rank=1600, winner=PLAYER_A, penalize_loser=True):
    if winner is PLAYER_A:
        winner_rank, loser_rank = player_a_rank, player_b_rank
    else:
        winner_rank, loser_rank = player_b_rank, player_a_rank
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
    if winner is PLAYER_A:
        return (new_winner_rank, new_loser_rank)
    return (new_loser_rank, new_winner_rank)


#this finds the bots in your rgkit directory
bots=[]
path='./robots/'
bdir=os.listdir(path)
for fn in bdir:
    bots.append(fn)
print bots
print '#of bots',len(bots)

botscores={}
for bot in bots:
    botscores[bot]=1200.0

pall = re.compile('\d+')

def play_match(bot1,bot2):
    p = subprocess.Popen('python run.py -H '+os.path.join(path, bot1)+' '+os.path.join(path, bot2), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        #print line
        #if len(line)<9 and len(line)>4:
        if line.startswith('['):
            scores=pall.findall(line)
            wn=0
            if int(scores[0])>int(scores[1]):
                wn=PLAYER_A
            elif int(scores[1])>int(scores[0]):
                wn=PLAYER_B
            if wn>0:
                newelo1,newelo2=calculate_elo_rank(botscores[bot1], botscores[bot2], winner=wn, penalize_loser=True)
                botscores[bot1]=float(newelo1)
                botscores[bot2]=float(newelo2)
            print bot1,bot2,scores,botscores[bot1],botscores[bot2]

    return p.wait()

#this plays the matches and records the scores as a percent win
#for i in range(number_of_matches):
#    random.shuffle(bots)
#    bot1=bots[0]
#    bot2=bots[1]
for k in range(number_of_matches):
    for i in range(len(bots)):
        for j in range(len(bots)):
            if i != j:
                retval = play_match(bots[i], bots[j])
    
#show results
for bot in botscores:
    print bot,botscores[bot]
