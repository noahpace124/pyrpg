#import
from random import randint

def crit(attacker):
    if randint(1, 100) <= attacker.get_lck():
        return True
    else:
        return False
        