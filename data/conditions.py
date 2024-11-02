#Import

class Condition:
    all_conditions = []

    def __init__(self, name, type, desc, duration_type, duration, stat='none', multiplier=1, func=None):
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
    def get_condition(cls, condition_name):
        for condition in cls.all_conditions:
            if condition.name == condition_name:
                return condition
        return None

#Note all duration in turns need to start at +1 because it removes a use the same turn it is applied
conditions = [
    Condition(
        name="Defense Down",
        type="debuff",
        desc="Cuts defense in half.",
        duration_type='turn',
        duration=4,
        stat='df',
        multiplier=0.5
    )
]