#Import
from helper import Helper

class Condition:
    all_conditions = []

    def __init__(self, name, type, desc, stat='none', multiplier=1, duration=1, duration_type='turn', func=None):
        self.name = name
        self.type = type
        self.desc = desc
        self.stat = stat
        self.multiplier = multiplier
        self.duration = duration
        self.duration_type = duration_type
        self.func = func
        Condition.all_conditions.append(self)
    
    @classmethod
    def get_condition(cls, condition_name, duration=0):
        for condition in cls.all_conditions:
            if condition.name == condition_name:
                condition.duration=duration
                return condition
        return None

#Note all duration in turns need to start at +1 because it removes a use the same turn it is applied
conditions = [
    Condition(
        name="Strength Down",
        type="debuff",
        desc="Cuts strength.",
        stat='str',
        multiplier=0.77
    ),
    Condition(
        name="Strength Up",
        type="buff",
        desc="Raises strength.",
        stat='str',
        multiplier=1.33
    ),
    Condition(
        name="Defense Down",
        type="debuff",
        desc="Cuts defense.",
        stat='df',
        multiplier=0.77
    ),
    Condition(
        name="Defense Up",
        type="buff",
        desc="Raises defense.",
        stat='df',
        multiplier=1.33
    ),
    Condition(
        name="Magic Down",
        type="debuff",
        desc="Cuts magic.",
        stat='mag',
        multiplier=0.77
    ),
    Condition(
        name="Magic Up",
        type="buff",
        desc="Raises magic.",
        stat='mag',
        multiplier=1.33
    ),
    Condition(
        name="Magical Defense Down",
        type="debuff",
        desc="Cuts magic defense.",
        stat='mdf',
        multiplier=0.77
    ),
    Condition(
        name="Magical Defense Up",
        type="buff",
        desc="Raises magic defense.",
        stat='mdf',
        multiplier=1.33
    ),
    Condition(
        name="Dexterity Down",
        type="debuff",
        desc="Cuts dexterity.",
        stat='dex',
        multiplier=0.77
    ),
    Condition(
        name="Dexterity Up",
        type="buff",
        desc="Raises dexterity.",
        stat='dex',
        multiplier=1.33
    ),
    Condition(
        name="Intelligence Down",
        type="debuff",
        desc="Cuts intelligence.",
        stat='int',
        multiplier=0.77
    ),
    Condition(
        name="Intelligence Up",
        type="buff",
        desc="Raises intelligence.",
        stat='int',
        multiplier=1.33
    ),
    Condition(
        name="Luck Down",
        type="debuff",
        desc="Cuts luck.",
        stat='lck',
        multiplier=0.77
    ),
    Condition(
        name="Luck Up",
        type="buff",
        desc="Raises luck.",
        stat='lck',
        multiplier=1.33
    ),
    Condition(
        name="Poison",
        type="debuff",
        desc="Damages the target in between turns.",
        stat='hp',
        multiplier=5
    )
]