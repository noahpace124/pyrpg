#Imports
import random

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
        return None  # or raise an exception if the spell isn't found

spells = [
    Spell(
        name='Fireball',
        desc='Hurl a ball of flame at the enemy.',
        type='Evocation',
        cost=8,
        matkmin=8,
        matkmax=14,
        reqm=3
    )
]