#import
from random import randint

def crit(attacker, defender):
    crit_chance = max(attacker.get_lck() - defender.get_lck(), 1) #always at least 1
    if randint(1, 100) <= crit_chance:
        return True
    else:
        return False
        