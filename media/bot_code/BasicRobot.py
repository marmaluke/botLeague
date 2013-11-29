'''
Created on 19/11/2013

@author: markl
'''
import rg

class Robot(object):
    '''
    Starting robot
    '''

    def act(self, game):
        # stay in the centre if we're already there
        if self.location == rg.CENTER_POINT:
            return ['guard']
        
        # attack if any enemies are nearby
        for loc, bot in game['robots'].iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]
                
        # move towards the centre
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]