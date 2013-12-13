#!python
import os
import ast
import argparse
###
import game

parser = argparse.ArgumentParser(description="Robot game execution script.")
parser.add_argument("usercode1",
                    help="File containing first robot class definition.")
parser.add_argument("usercode2",
                    help="File containing second robot class definition.")
args = parser.parse_args()

def make_player(fname):
    return game.Player(open(fname).read())

if __name__ == '__main__':

    map_name = os.path.join(os.path.dirname(__file__), 'maps/default.py')
    map_data = ast.literal_eval(open(map_name).read())
    game.init_settings(map_data)

    players = [game.Player(open(args.usercode1).read()),
               game.Player(open(args.usercode2).read())]
    g = game.Game(*players, print_info=False, record_actions=True, record_history = True)
    g.run_all_turns()
    
    print "history={0}".format(g.history)
    print "scores={0}".format(g.get_scores())
