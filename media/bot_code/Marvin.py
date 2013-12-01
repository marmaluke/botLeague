'''
Created on 19/11/2013

@author: markl
'''

import rg

class Robot(object):
    '''
    Looks for enemy robots and moves toward them.
    This is a refinement of the basic Hunter that suicides if its health is too low.
    '''
    
    def __get_neighbours(self, game):
        return [bot for (loc, bot) in game['robots'].items() if rg.dist(self.location, loc) <= 1 and self.location != loc]

    def act(self, game):
        num_ememies = self.__count_neighbouring_enemies(game)
        # attack nearby robot 
        for loc, bot in game['robots'].iteritems():
            if bot.player_id != self.player_id:
                if rg.wdist(loc, self.location) <= 1:
                    if num_ememies * 15 > self.hp:
                        #print "My health = {}, expected damage = {}, suiciding".format(str(self.hp), str(num_ememies * 15))
                        return ['suicide']
                    else:
                        return ['attack', loc]

        # swarm enemy robot
        for loc, bot in game['robots'].iteritems():
            if bot.player_id != self.player_id:
                return ['move', rg.toward(self.location, loc)]
                
        # no enemies? guard
        #return ['guard']
        # no enemies? move towards the centre
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]
    
    def __get_neighbouring_enemies(self, game):
        return [bot for bot in self.__get_neighbours(game) if bot.player_id != self.player_id]
    
    def __count_neighbouring_enemies(self, game):
        return len(self.__get_neighbouring_enemies(game))