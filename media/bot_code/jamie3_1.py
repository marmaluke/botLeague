import rg
from Queue import PriorityQueue
from random import choice

WIDTH = 19
HEIGHT = 19

BLOCKED = 0
MOVE_NEXT_TO_IDLE_FRIEND = 0
MOVE_TO_MULTIPLE_ENEMIES = 0

GUARD = 1
DEFAULT = 1

MOVE_TO_NEAR_FRIEND = 2

MOVE_TO_ENEMY = 5
MOVE_NEXT_TO_ATTACKING_FRIEND = 6
MOVE_NEXT_TO_ATTACKING_FRIEND_NEAR_ATTACKER = 7
MOVE_TO_ENEMY_BEING_ATTACKED = 8
ATTACK = 10
SUICIDE = 15

def debug(string):
	#print string

class Robot:
	
	def act(self, game):
		debug("Act: %s" % (self.location,))
	
		self.game = game
			
	  #Movement
		possibleMoves = map(lambda x: (self.rateLoc(x), ['move', x]), rg.locs_around(self.location, filter_out=['obstacle', 'invalid', 'spawn']))
		
		#Guard
		possibleMoves.append((GUARD , ['guard']))
		
		#Attack
		enemyLocs = filter(lambda x: x in self.game.robots and self.game.robots[x].player_id != self.player_id, rg.locs_around(self.location))
		possibleMoves.extend(map(lambda x: (ATTACK, ['attack', x]), enemyLocs))
		
		#Suicide
		if enemyLocs > 1 and self.hp < 15:
			possibleMoves.append((SUICIDE, ['suicide']))
		
		debug("PossibleMoves: %s" % possibleMoves)
		
		bestScore = reduce(lambda x,y: x if x[0] >= y[0] else y, possibleMoves)[0]
	
					
		bestMoves = map(lambda x: x[1], filter(lambda x: x[0] == bestScore, possibleMoves))
		randomMove = choice(bestMoves)
		
		debug("Move: %s" % randomMove)
		
		return randomMove
		
	def rateLoc(self, loc):
	
		debug("Rating location: %s" % (loc,))

		if loc in self.game.robots:
			debug("Blocked")
			return BLOCKED	
				
		adjacentFriends = self.adjacentFriends(loc)
		adjacentEnemies = self.adjacentEnemies(loc)
				
		if len(adjacentFriends) > 0:
			idleFriends = filter(lambda x: len(self.adjacentEnemies(x)) == 0, adjacentFriends)
			if len(idleFriends) == 0:
				debug("MOVE_NEXT_TO_IDLE_FRIEND")
				return MOVE_NEXT_TO_IDLE_FRIEND
			elif len(self.nearAttackers(loc)) > 0:
				debug("MOVE_NEXT_TO_ATTACKING_FRIEND_NEAR_ATTACKER")
				return MOVE_NEXT_TO_ATTACKING_FRIEND_NEAR_ATTACKER
			else:
				debug("MOVE_NEXT_TO_ATTACKING_FRIEND")
				return MOVE_NEXT_TO_ATTACKING_FRIEND
		
		if len(adjacentEnemies) == 1:
			if len(self.adjacentFriends(adjacentEnemies[0])) > 0:
				debug("MOVE_TO_ENEMY_BEING_ATTACKED")
				return MOVE_TO_ENEMY_BEING_ATTACKED
			else:
				debug("MOVE_TO_ENEMY")
				return MOVE_TO_ENEMY
		
		if len(adjacentEnemies) > 1:
			debug("MOVE_TO_MULTIPLE_ENEMIES")
			return MOVE_TO_MULTIPLE_ENEMIES
		
		if self.nearFriends(loc):
			debug("MOVE_TO_NEAR_FRIEND")
			return MOVE_TO_NEAR_FRIEND
		
		debug("DEFAULT")
		return DEFAULT
	
	def adjacentEnemies(self, loc):
		return filter(lambda x: x in self.game.robots and self.game.robots[x].player_id != self.player_id, rg.locs_around(loc))
		
	def adjacentFriends(self, loc):
		return filter(lambda x: x in self.game.robots and self.game.robots[x].player_id == self.player_id and x != self.location, rg.locs_around(loc))
	
	def nearFriends(self, loc):
		return filter(lambda x: self.game.robots[x].player_id == self.player_id and x != self.location and rg.wdist(x, loc) == 2, self.game.robots)
		
	def nearAttackers(self, loc):
		return filter(lambda x: self.game.robots[x].player_id != self.player_id and rg.wdist(x, loc) == 2, self.game.robots)
	

		
	