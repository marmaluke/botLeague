import rg
import random

class Robot:
    _markp = 0
    def act(self, game):
        try:
            _markp
        except NameError:
            _markp = random.randint(1,2)

 
        # if there are enemies around, attack them
        friendlies = []
        for loc, bot in game['robots'].iteritems():
            if bot.player_id == self.player_id:
                friendlies.append((loc, bot))

        
        end_locations = []
        for loc, bot in friendlies:
            if loc == self.location:
                continue
            result = do_move(bot, self.player_id, loc, game, _markp)
            if result[0] == 'move':
                end_locations.append(result[1])


        cur_result = do_move(self, self.player_id, self.location, game, _markp)

        if cur_result[0] == 'move' and len(end_locations) > 1:
            for loc in end_locations:
                if cur_result[1] == loc[0] and cur_result[2] == loc[1]:
                    return ['guard']

        return cur_result
            


def do_move(current_bot, player_id, location, game, _markp):
        adjacent_enemies = []
        for loc, bot in game['robots'].iteritems():
            if bot.player_id != player_id:
                if rg.wdist(loc, location) <= 1:
                    adjacent_enemies.append((loc, bot))

        if(len(adjacent_enemies) < 1):
            # if we're in the center and there are no enemies around, stay put
            if current_bot.location == rg.CENTER_POINT:
                return ['guard']

        else:
            if current_bot.hp < len(adjacent_enemies)*9:
                    return ['suicide']
            else:
                min_strength = 51
                attack_loc = ""
                for loc, bot in adjacent_enemies:
                    if bot.hp < min_strength:
                        attack_loc = loc
                        min_strength = bot.hp

                return ['attack', attack_loc]

        # move toward the center
        if _markp == 1:
            return ['move', rg.toward(location, rg.CENTER_POINT)]
        else:
            return ['move', alt_toward(location, rg.CENTER_POINT)]
 


def alt_toward(curr, dest):
    if curr == dest:
        return curr

    x0, y0 = curr
    x, y = dest
    x_diff, y_diff = x - x0, y - y0

    if abs(y_diff) < abs(x_diff):
        return (x0 + x_diff / abs(x_diff), y0)
    return (x0, y0 + y_diff / abs(y_diff))

