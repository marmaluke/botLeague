import rg
from Queue import PriorityQueue
from random import choice

WIDTH = 19
HEIGHT = 19

BLOCKED = 0
MOVE_TO_MULTIPLE_ENEMIES = 0

GUARD = 2
DEFAULT = 1

MOVE_TO_NEAR_FRIEND = 2
MOVE_NEXT_TO_FRIEND = 3
MOVE_NEXT_TO_ENEMY = 4
MOVE_TO_NEAR_ENEMY = 3
MOVE_NEXT_TO_ATTACKED_ENEMY = 11

ATTACK_ENEMY = 10
ATTACK_ATTACKED_ENEMY = 12
SUICIDE = 15

def debug(string):
	pass
	#print string

def findAdjacentEnemies(loc, robot, game):
	return filter(lambda x: x in game.robots and game.robots[x].player_id != robot.player_id, rg.locs_around(loc))
	
def findAdjacentFriends(loc, robot, game):
	return filter(lambda x: x in game.robots and game.robots[x].player_id == robot.player_id and x != robot.location, rg.locs_around(loc))
	
def findNearEnemies(loc, robot, game):
	return filter(lambda x: game.robots[x].player_id != robot.player_id and rg.wdist(x, loc) == 2, game.robots)

def findNearFriends(loc, robot, game):
	return filter(lambda x: game.robots[x].player_id == robot.player_id and x != robot.location and rg.wdist(x, loc) == 2, game.robots)


def rateLoc(loc, robot, game):	
	debug("Rating location: %s" % (loc,))

	if loc in game.robots:
		debug("Blocked")
		return BLOCKED	
			
	adjacentFriends = findAdjacentFriends(loc, robot, game)
	adjacentEnemies = findAdjacentEnemies(loc, robot, game)
	nearFriends = findNearFriends(loc, robot, game)
	nearEnemies = findNearEnemies(loc, robot, game)
	
	score = DEFAULT
			
	if len(adjacentFriends) > 0:
		debug("MOVE_NEXT_TO_FRIEND")
		score += MOVE_NEXT_TO_FRIEND
	
	if len(nearFriends) > 0:
		debug("MOVE_TO_NEAR_FRIEND")
		score += MOVE_TO_NEAR_FRIEND
		
	if len(adjacentEnemies) > 0:
		attackedEnemies = filter(lambda enemy: len(findAdjacentFriends(enemy, robot, game)) > 0, adjacentEnemies)
		if len(attackedEnemies) > 0:
			debug("MOVE_NEXT_TO_ATTACKED_ENEMY")
			score += MOVE_NEXT_TO_ATTACKED_ENEMY
		else:
			debug("MOVE_NEXT_TO_ENEMY")
			score += MOVE_NEXT_TO_ENEMY
		
	
	if len(nearEnemies) > 0:
		debug("MOVE_TO_NEAR_ENEMY")
		score += MOVE_TO_NEAR_ENEMY
	
	
	
	
	return score


def getMoves(robot, game):		

	#TODO if noone near, move to closest friend
		
	#Movement
	possibleMoves = map(lambda x: (rateLoc(x, robot, game), ['move', x]), rg.locs_around(robot.location, filter_out=['obstacle', 'invalid']))
	
	#Guard
	possibleMoves.append((GUARD , ['guard']))
	
	#Attack
	enemies = findAdjacentEnemies(robot.location, robot, game)
	for enemy in enemies:
		if len(findAdjacentFriends(enemy, robot, game)) > 0:
			possibleMoves.append((ATTACK_ATTACKED_ENEMY, ['attack', enemy]))
		else:
			possibleMoves.append((ATTACK_ENEMY, ['attack', enemy]))
	
	#Suicide
	if len(enemies) > 0 and findAdjacentFriends(robot.location, robot, game) == 0 and robot.hp < 12:
		possibleMoves.append((SUICIDE, ['suicide']))
	
	possibleMoves = sorted(possibleMoves, key=lambda x: x[0], reverse=True)
	debug("PossibleMoves: %s" % possibleMoves)
		
	return possibleMoves
	
def calculateBestMoves(everyonesMoves):
	bestMoves = map(lambda x: x[0][1], everyonesMoves.values())
	
	for me in sorted(everyonesMoves.keys()):
			myMove = everyonesMoves[me][0][1]
			if myMove[0] != 'move':
				continue
			
			for them in everyonesMoves.keys():
				if them == me:
					continue
				theirMove = everyonesMoves[them][0][1]
				if theirMove[0] == 'move' and theirMove[1] == myMove[1]:
					del everyonesMoves[them][0]
	
	return dict((loc, everyonesMoves[loc][0][1]) for loc in everyonesMoves.keys())

class Robot:
	
	def act(self, game):
		debug("Act: %s" % (self.location,))
		
		myRobotLocs = filter(lambda x: game.robots[x].player_id == self.player_id, game.robots)
		
		everyonesMoves = dict((loc, getMoves(game.robots[loc], game)) for loc in myRobotLocs)
		
		myMove = calculateBestMoves(everyonesMoves)[self.location]
			
		debug("Move: %s" % myMove)
		
		return myMove
		
	
	

		
	