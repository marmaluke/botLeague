import rg
import random

class Robot:
    _markp = 0
    def act(self, game):
        try:
            _markp
        except NameError:
            _markp = random.randint(1,2)

        # if we're in the center, stay put
        if self.location == rg.CENTER_POINT:
            return ['guard']

        # if there are enemies around, attack them
        adjacent = []
        for loc, bot in game['robots'].iteritems():
            if bot.player_id != self.player_id:
                if rg.wdist(loc, self.location) <= 1:
                    adjacent.append((loc, bot))
        
        if len(adjacent) >= 1:
			if current_bot.hp < len(adjacent_enemies)*9:
                return ['suicide']
            else:
                min_strength = 51;
                attack_loc = "";
                for loc, bot in adjacent:
                    if bot.hp < min_strength:
                        attack_loc = loc
                        min_strength = bot.hp

                return ['attack', attack_loc]

        # move toward the center
        if _markp == 1:
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        else:
            return ['move', alt_toward(self.location, rg.CENTER_POINT)]
 


def alt_toward(curr, dest):
    if curr == dest:
        return curr

    x0, y0 = curr
    x, y = dest
    x_diff, y_diff = x - x0, y - y0

    if abs(y_diff) < abs(x_diff):
        return (x0 + x_diff / abs(x_diff), y0)
    return (x0, y0 + y_diff / abs(y_diff))
