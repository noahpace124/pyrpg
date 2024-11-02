#Imports
from random import randint

class Skill:
    all_skills = []  # Class-level attribute to hold all skill instances

    def __init__(self, name, desc, cost, type, reqa, reqm, func=None):
        self.name = name
        self.desc = desc
        self.cost = cost
        self.type = type
        self.reqa = reqa
        self.reqm = reqm
        self.func = func  # Add a reference to the skill function
        Skill.all_skills.append(self)  # Automatically add the instance to the class-level list

    def __repr__(self):
        return (f"<Skill(name={self.name}, desc={self.desc}, cost={self.cost}, "
                f"reqa={self.reqa}, reqm={self.reqm}, reta={self.reta}, skill_func={self.skill_func})>")

    @classmethod
    def get_skill(cls, skill_name):
        for skill in cls.all_skills:
            if skill.name == skill_name:
                return skill
        return None  # or raise an exception if the skill isn't found

#Redefined these to prevent circular import
def crit(attacker, defender):
    return (get_crit_rate(attacker, defender) >= randint(1, 100))

def get_crit_rate(attacker, defender): #always returns at least 1
    return max(round(((attacker.lck * 2) / 100) * ((attacker.lvl/defender.lvl) * 100)), 1)

# Define skill functions
def instant_recharge(attacker, defender):
    amount = attacker.mp - attacker.cmp
    if amount > attacker.ctp: #use remaining tp
        attacker.cmp += attacker.ctp
        attacker.ctp -= attacker.ctp
    else: #use only required tp
        attacker.cmp += amount
        attacker.ctp -= amount
    if attacker.cmp == attacker.mp:
        input(f"{attacker.name} recharged their MP fully.")
    else:
        input(f"{attacker.name} recharged their MP somewhat.")

def heavy_blow(attacker, defender):
    attacker.ctp -= 10
    atk = round((attacker.str * 2) * 1.5) + randint(attacker.EQweapon.atkmin, attacker.EQweapon.atkmax)
    if crit(attacker, defender):
        print("Critical Hit!")
        atk = atk * 3
    df = defender.get_df(atk)
    dmg = max(atk - df, 1)
    defender.chp -= dmg
    input(f"{attacker.name} landed a heavy blow on {defender.name} for {dmg} damage.")

def quick_strike(attacker, defender):
    attacker.ctp -= 10
    atk = attacker.get_atk()
    if crit(attacker, defender):
        print("Critical Hit!")
        atk = atk * 3
    df = defender.get_df(atk)
    dmg = max(atk - df, 1)
    defender.chp -= dmg
    input(f"{attacker.name} striked quickly at {defender.name} for {dmg} damage.")

# Create skill instances
skills = [
    Skill(
        name='Instant Recharge',
        desc='Use your TP to instantly recharge your MP. Converts TP to MP.',
        cost=1,
        type='instant',
        reqa='int',
        reqm=3,
        func=instant_recharge
    ),
    Skill(
        name='Heavy Blow',
        desc='Strike with concentrated effort. Use 1.5 times your str on this attack.',
        cost=10,
        type='instant',
        reqa='str',
        reqm=3,
        func=heavy_blow
    ),
    Skill(
        name='Quick Strike',
        desc='Strike first. This attack will always land first.',
        cost=10,
        type='priority',
        reqa='dex',
        reqm=3,
        func=quick_strike
    )
]