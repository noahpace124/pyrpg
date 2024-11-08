#Import
from random import randint, choice

#Import from File
from helper import Helper
from .weapons import Weapon
from .armors import Armor
from .crit import crit

class Enemy:
    def __init__(self, name, con, mag, str, int, dex, lck, df, mdf, weapon=Weapon.get_weapon('None'), armor=Armor.get_armor('None'), skills=[], spells=[], conditions=[], flags=[]):
        self.name = name

        self.lvl = con + mag + str + int + dex + lck
        self.hp = max(20 + ((con - 1) * 5), 1)
        self.chp = self.hp
        self.mp = max(10 + ((int - 1) * 5), 0)
        self.cmp = self.mp
        self.tp = max(10 + ((dex - 1) * 5), 0)
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

        self.skills = skills
        self.spells = spells

        self.conditions = conditions
        self.flags = flags
    
    def view_stats(self):
        Helper.clear_screen()
        Helper.make_banner(f"{self.name}'s Stats")
        
        # Display enemy attributes
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
        if self.EQweapon.stat == 'str':
            stat = self.get_str() * 2
        else:   #stat == dex
            stat = self.get_dex()
        atk = max(stat + randint(self.EQweapon.atkmin, self.EQweapon.atkmax), 1)
        if crit(self):
            print("Critical Hit!")
            atk = atk * 2
        return atk
    
    def get_df(self, atk):
        percentage_df = round(atk * (self.df / 100))
        total_defense = round((percentage_df + self.EQarmor.df ) * self.get_condition_multiplier('df'))
        return max(0, total_defense)  # Ensure the defense value doesn't drop below 0

    def get_matk(self, spell):
        matk = max(((self.get_mag() * 2) + randint(spell.matkmin, spell.matkmax) + randint(self.EQweapon.matkmin, self.EQweapon.matkmax)), 1)
        if crit(self):
            print("Critical Hit!")
            matk = matk * 2
        return matk

    def get_mdf(self, matk):
        percentage_mdf = round(matk * (self.mdf / 100))
        total_magic_defense = round((percentage_mdf + self.EQarmor.mdf ) * self.get_condition_multiplier('mdf'))
        return max(0, total_magic_defense) #Ensure the magic defense value doesn't drop below 0

    def get_str(self):
        return round(self.str * self.get_condition_multiplier('str'))

    def get_dex(self):
        return round(self.dex * self.get_condition_multiplier('dex'))

    def get_mag(self):
        return round(self.mag * self.get_condition_multiplier('mag'))

    def get_int(self):
        return round(self.int * self.get_condition_multiplier('int'))

    def get_lck(self):
        return round(self.lck * self.get_condition_multiplier('lck'))

    def get_spd(self):
        return max((self.get_dex() * 2) + max(0, self.get_lck()), 0)

    def get_condition_multiplier(self, stat):
        multiplier = 1
        for condition in self.conditions:
            if condition and condition.stat == stat:
                multiplier *= condition.multiplier
        return multiplier

    def get_dodge(self):
        return self.get_dex() + randint(0, self.get_lck())

    def get_action(self): #returns the enemy object
        skill_options = []
        spell_options = []
        if len(self.skills) > 0:
            for skill in self.skills:
                if self.ctp >= skill.cost:
                    skill_options.append(skill)
        if len(self.spells) > 0:
            for spell in self.spells:
                if self.cmp >= spell.cost:
                    spell_options.append(spell)
        if self.str == self.mag:
            if self.dex == self.mag:
                if (self.dex + self.str) >= (self.mag + self.int) and len(skill_options) > 0:
                    return choice(skill_options)
                elif (self.mag + self.int) >= (self.str + self.dex) and len(spell_options) > 0:
                    return choice(spell_options)
                else:
                    return None
            elif self.dex > self.mag and len(skill_options) > 0:
                return choice(skill_options)
            elif self.mag > self.dex and len(spell_options) > 0:
                return choice(spell_options)
            else:
                return None
        if self.str > self.mag and len(skill_options) > 0:
            return choice(skill_options)
        elif self.mag > self.str and len(spell_options) > 0:
            return choice(spell_options)
        else:
            return None

    def upkeep(self):
        self.ctp += max(self.get_dex(), 0)
        if self.ctp > self.tp:
            self.ctp = self.tp
        self.cmp += max(self.get_int(), 0)
        if self.cmp > self.mp:
            self.cmp = self.mp
        for condition in self.conditions:
            if condition and condition.duration_type == 'turn':
                condition.duration -= 1
                if condition.duration == 0:
                    self.conditions.remove(condition)