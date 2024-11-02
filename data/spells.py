#Imports
from random import randint

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

    def __repr__(self):
        return f"<Spell(name={self.name}, desc={self.desc}, cost={self.cost}, matkmin={self.matkmin}, matkmax={self.matkmax}, reqm={self.reqm})>"
    
    @classmethod
    def get_spell(cls, spell_name):
        for spell in cls.all_spells:
            if spell.name == spell_name:
                return spell
        return None

#Redefined these to prevent circular import
def crit(attacker, defender):
    return (get_crit_rate(attacker, defender) >= randint(1, 100))

def get_crit_rate(attacker, defender): #always returns at least 1
    return max(round(((attacker.lck * 2) / 100) * ((attacker.lvl/defender.lvl) * 100)), 1)

def fireball(attacker, defender):
    attacker.cmp -= 10
    matk = attacker.get_matk(Spell.get_spell('Fireball'))
    if crit(attacker, defender):
        print("Critical Hit!")
        matk = matk * 2
    mdf = defender.get_mdf(matk)
    dmg = max(matk - mdf, 1)
    defender.chp -= dmg
    input(f"{attacker.name} cast Fireball on {defender.name} for {dmg} damage.")


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
    )
]