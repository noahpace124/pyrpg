#Imports
from random import randint

from helper import Helper

class Spell:
    all_spells = []  # Class-level attribute to hold all spell instances

    def __init__(self, name, desc, type, cost, matkmin, matkmax, reqm, func=None):
        self.name = name
        self.desc = desc
        self.type = type
        self.cost = cost
        self.matkmin = matkmin
        self.matkmax = matkmax
        self.reqm = reqm
        self.func = func
        Spell.all_spells.append(self)  # Automatically add the instance to the class-level list
    
    @classmethod
    def get_spell(cls, spell_name):
        for spell in cls.all_spells:
            if spell.name == spell_name:
                return spell
        print('Error')
        return None

def fireball(attacker, defender):
    print(f"{attacker.name} casts Fireball.")
    attacker.cmp -= 10
    dodge_chance = max(defender.get_dodge() - attacker.get_dex(), 0)
    if randint(1, 100) > dodge_chance:
        matk = attacker.get_matk(Spell.get_spell('Fireball'))
        mdf = defender.get_mdf(matk)
        dmg = max(matk - mdf, 1)
        defender.chp -= dmg
        input(f"{attacker.name} cast Fireball on {defender.name} for {Helper.string_color(dmg, 'r')} damage.")
    else:
        input(f"{defender.name} avoided {attacker.name}\'s Fireball!")

def zap(attacker, defender):
    print(f"{attacker.name} casts Zap.")
    attacker.cmp -= 5
    dodge_chance = max(defender.get_dodge() - attacker.get_dex(), 0)
    if randint(1, 100) > dodge_chance:
        matk = attacker.get_matk(Spell.get_spell('Zap'))
        mdf = defender.get_mdf(matk)
        dmg = max(matk - mdf, 1)
        defender.chp -= dmg
        input(f"{attacker.name} cast Zap on {defender.name} for {Helper.string_color(dmg, 'r')} damage.")
    else:
        input(f"{defender.name} avoided {attacker.name}\'s Zap!")


spells = [
    Spell(
        name='Fireball',
        desc='Hurl a ball of flame at the enemy.',
        type='instant',
        cost=10,
        matkmin=8,
        matkmax=14,
        reqm=3,
        func=fireball
    ),
    Spell(
        name='Zap',
        desc='Shock your enemy with a quick small bolt of lightning.',
        type='instant',
        cost=5,
        matkmin=4,
        matkmax=7,
        reqm=2,
        func=zap
    )
]