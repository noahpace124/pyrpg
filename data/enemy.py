#Import
from random import randint

#Import from File
from helper import Helper
from .weapons import Weapon
from .armors import Armor

class Enemy:
    def __init__(self, name, con, mag, str, int, dex, lck, df, mdf, weapon=Weapon.get_weapon('None'), armor=Armor.get_armor('None'), spells=[], skills=[], conditions=[], flags=[]):
        self.name = name

        self.lvl = con + mag + str + int + dex + lck
        self.hp = 20 + ((con - 1) * 5)
        self.chp = self.hp
        self.mp = 10 + ((int - 1) * 5)
        self.cmp = self.mp
        self.tp = 10 + ((dex - 1) * 5)
        self.ctp = self.tp

        self.con = con
        self.mag = mag
        self.str = str
        self.int = int
        self.dex = dex
        self.lck = lck

        self.df = df
        self.mdf = mdf

        self.EQweapon = weapon
        self.EQarmor = armor

        self.spells = spells
        self.skills = skills

        self.conditions = conditions
        self.flags = flags
    
    def view_stats(self):
        Helper.clear_screen()
        Helper.make_banner(f"{self.name}'s Stats")
        
        # Display player attributes
        print(f"HP: {self.chp}/{self.hp}")
        print(f"MP: {self.cmp}/{self.mp}")
        print(f"TP: {self.ctp}/{self.tp}")
        print(f"Strength: {self.str}")
        print(f"Constitution: {self.con}")
        print(f"Magic: {self.mag}")
        print(f"Intelligence: {self.int}")
        print(f"Dexterity: {self.dex}")
        print(f"Luck: {self.lck}")
        print(f"Physical Defense: {self.df}")
        print(f"Magical Defense: {self.mdf}")

        # Display equipped weapon details
        print(f"Equipped Weapon: {self.EQweapon.name}")

        # Display equipped armor details
        print(f"Equipped Armor: {self.EQarmor.name}")

        # Display equipped spell and skill details
        equipped_spells = [spell.name for spell in self.spells]
        print(f"Prepaired Spells: {', '.join(equipped_spells)}")
        equipped_skills = [skill.name for skill in self.skills]
        print(f"Prepaired Skills: {', '.join(equipped_skills)}")

        # Display status conditions
        status_conditions = []
        for condition in self.conditions:
            condition_info = f"{condition.name}: {condition.duration} {condition.duration_type}"
            status_conditions.append(condition_info)
        print(f"Conditions: {', '.join(status_conditions)}\n")

        input("(Press enter to continue...) ")
    
    def get_atk(self):
        return (self.str * 2) + randint(self.EQweapon.atkmin, self.EQweapon.atkmax)
    
    def get_df(self, atk):
        percentage_df = round(atk * (self.df / 100))
        total_defense = round((percentage_df + self.EQarmor.df ) * self.get_condition_multiplier('df'))
        return max(0, total_defense)  # Ensure the defense value doesn't drop below 0

    def get_matk(self, spell):
        return (self.mag * 2) + randint(spell.matkmin, spell.matkmax) + randint(self.EQweapon.matkmin, self.EQweapon.matkmax)

    def get_mdf(self, ematk):
        percentage_mdf = round((ematk * (self.mdf / 100)))
        return percentage_mdf + self.EQarmor.mdf

    def get_spd(self):
        return (self.dex * 2) + max(0, self.lck)

    def get_condition_multiplier(self, stat):
        multiplier = 1
        for condition in self.conditions:
            if condition.stat == stat:
                multiplier *= condition.multiplier
        return multiplier

    def upkeep(self):
        self.ctp += self.dex
        if self.ctp > self.tp:
            self.ctp = self.tp
        self.cmp += self.int
        if self.cmp > self.mp:
            self.cmp = self.mp
        for condition in self.conditions:
            if condition.duration_type == 'turn':
                condition.duration -= 1
                if condition.duration == 0:
                    self.conditions.remove(condition)