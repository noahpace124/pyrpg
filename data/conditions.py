#Import

class Condition:
    all_conditions = []

    def __init__(self, name, type, desc, duration_type, stat='none', multiplier=1, duration=0, func=None):
        self.name = name
        self.type = type
        self.desc = desc
        self.duration_type = duration_type
        self.duration = duration
        self.stat = stat
        self.multiplier = multiplier
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
        name="Attack Down",
        type="debuff",
        desc="Cuts attack.",
        duration_type='turn',
        stat='atk',
        multiplier=0.77
    ),
    Condition(
        name="Attack Up",
        type="buff",
        desc="Raises attack.",
        duration_type='turn',
        stat='atk',
        multiplier=1.33
    ),
    Condition(
        name="Defense Down",
        type="debuff",
        desc="Cuts defense.",
        duration_type='turn',
        stat='df',
        multiplier=0.77
    ),
    Condition(
        name="Defense Up",
        type="buff",
        desc="Raises defense.",
        duration_type='turn',
        stat='df',
        multiplier=1.33
    ),
    Condition(
        name="Magic Attack Down",
        type="debuff",
        desc="Cuts magic attack.",
        duration_type='turn',
        stat='matk',
        multiplier=0.77
    ),
    Condition(
        name="Magic Attack Up",
        type="buff",
        desc="Raises magic attack.",
        duration_type='type',
        stat='matk',
        multiplier=1.33
    ),
    Condition(
        name="Magical Defense Down",
        type="debuff",
        desc="Cuts magic defense.",
        duration_type='turn',
        stat='mdf',
        multiplier=0.77
    ),
    Condition(
        name="Magical Defense Up",
        type="buff",
        desc="Raises magic defense.",
        duration_type='turn',
        stat='mdf',
        multiplier=1.33
    ),
    Condition(
        name="Dexterity Down",
        type="debuff",
        desc="Cuts dexterity.",
        duration_type='turn',
        stat='dex',
        multiplier=0.77
    ),
    Condition(
        name="Dexterity Up",
        type="buff",
        desc="Raises dexterity.",
        duration_type='turn',
        stat='dex',
        multiplier=1.33
    ),
    Condition(
        name="Intelligence Down",
        type="debuff",
        desc="Cuts intelligence.",
        duration_type='turn',
        stat='int',
        multiplier=0.77
    ),
    Condition(
        name="Intelligence Up",
        type="buff",
        desc="Raises intelligence.",
        duration_type='turn',
        stat='int',
        multiplier=1.33
    ),
    Condition(
        name="Luck Down",
        type="debuff",
        desc="Cuts luck.",
        duration_type='turn',
        stat='lck',
        multiplier=0.77
    ),
    Condition(
        name="Luck Up",
        type="buff",
        desc="Raises luck.",
        duration_type='turn',
        stat='lck',
        multiplier=1.33
    )
]