#import
from random import randint

def crit(attacker, defender):
    return (get_crit_rate(attacker, defender) >= randint(1, 100))

def get_crit_rate(attacker, defender): #always returns at least 1
    return max(int(round(((attacker.get_lck() * 2) / 100) * ((attacker.lvl/defender.lvl) * 100), 0)), 1)