#Imports
from random import randint

#Imports from File
from .conditions import Condition

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

    @classmethod
    def get_skill(cls, skill_name):
        for skill in cls.all_skills:
            if skill.name == skill_name:
                return skill
        return None  # or raise an exception if the skill isn't found

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
    attacker.conditions.append(Condition.get_condition("Attack Up", 1))
    dodge_chance = max(defender.get_dodge() - attacker.get_dex(), 0)
    if randint(1, 100) > dodge_chance:
        atk = attacker.get_atk()
        df = defender.get_df(atk)
        dmg = max(atk - df, 1)
        defender.chp -= dmg
        input(f"{attacker.name} landed a heavy blow on {defender.name} for {dmg} damage.")
    else:
        input(f"{defender.name} avoided {attacker.name}\'s attack!")

def quick_strike(attacker, defender):
    attacker.ctp -= 10
    dodge_chance = max(defender.get_dodge() - attacker.get_dex(), 0)
    if randint(1, 100) > dodge_chance:
        atk = attacker.get_atk()
        df = defender.get_df(atk)
        dmg = max(atk - df, 1)
        defender.chp -= dmg
        input(f"{attacker.name} striked quickly at {defender.name} for {dmg} damage.")
    else:
        input(f"{defender.name} avoided {attacker.name}\'s attack!")

def damage_armor(attacker, defender):
    attacker.ctp -= 10
    attacker.conditions.append(Condition.get_condition("Attack Down", 1))
    dodge_chance = max(defender.get_dodge() - attacker.get_dex(), 0)
    if randint(1, 100) > dodge_chance:
        atk = attacker.get_atk()
        df = defender.get_df(atk)
        dmg = max(atk - df, 1)
        defender.chp -= dmg
        input(f"{attacker.name} tried to destroy some of {defender.name}\'s armor and did {dmg} damage.")
        apply = True
        for condition in defender.conditions: #check if we already have the condition
            if condition and condition.name == "Defense Down":
                condition.duration = 4
                apply = False
        if apply: #we don't have the condition
            defender.conditions.append(Condition.get_condition("Defense Down", 4))
        input(f"{attacker.name} lowered {defender.name}\'s defense.")
    else:
        input(f"{defender.name} avoided {attacker.name}\'s attack!")


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
        desc='Strike with concentrated effort. Use 1.33 times your str on this attack.',
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
    ),
    Skill(
        name='Damage Armor',
        desc='Strike powerfully into your enemy\'s armor to lower their Defense for 3 turns.',
        cost=10,
        type='instant',
        reqa='str',
        reqm='3',
        func=damage_armor
    )
]