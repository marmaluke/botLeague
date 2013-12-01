import rg
from Queue import PriorityQueue
from random import choice

WIDTH = 19
HEIGHT = 19

#Rate each spot around the bot and move to the best one

class Robot:
	
	def act(self, game):
		self.game = game
			
	  #Movement
		possibleMoves = map(lambda x: (self.rateLoc(x), ['move', x]), rg.locs_around(self.location, filter_out=['obstacle', 'invalid', 'spawn']))
		
		#Guard
		possibleMoves.append((1 , ['guard']))
		
		#Attack
		enemyLocs = filter(lambda x: x in self.game.robots and self.game.robots[x].player_id != self.player_id, rg.locs_around(self.location))
		possibleMoves.extend(map(lambda x: (10, ['attack', x]), enemyLocs))
		
		#Suicide
		if enemyLocs > 1 and self.hp < 15:
			possibleMoves.append((15, ['suicide']))
				
		bestScore = reduce(lambda x,y: x if x[0] >= y[0] else y, possibleMoves)[0]
	
					
		bestMoves = map(lambda x: x[1], filter(lambda x: x[0] == bestScore, possibleMoves))
		randomMove = choice(bestMoves)
			
		
		return randomMove
		
	def rateLoc(self, loc):		
		if loc in self.game.robots:
			return 0
		
		
		adjacentEnemies = filter(lambda x: x in self.game.robots and self.game.robots[x].player_id != self.player_id, rg.locs_around(loc))
		adjacentFriends = filter(lambda x: x in self.game.robots and self.game.robots[x].player_id == self.player_id and x != self.location, rg.locs_around(loc))
		
		
		
		if len(adjacentFriends) > 0:
			return 0
		
		if len(adjacentEnemies) == 1:
			return 5
		
		if len(adjacentEnemies) > 1:
			return 0
		
		return 1
	
	
		
	