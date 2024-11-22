#Import
from random import randint, choice

#Import from File
from helper import Helper
from .weapons import Weapon
from .armors import Armor

class Enemy:
    def __init__(self, name, con, mag, str, int, dex, lck, df, mdf, weapon=Weapon.get_weapon('None'), armor=Armor.get_armor('None'), skills=[], spells=[], inv=[], conditions=[], flags=[]):
        self.name = Helper.string_color(name, 'r')

        self.lvl = con + mag + str + int + dex + lck
        self.hp = 20 + (5 * con)
        self.chp = self.hp
        self.mp = int * 5
        self.cmp = self.mp
        self.tp = dex * 5
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

        self.inv = inv
        self.conditions = conditions
        self.flags = flags
    
    def view_stats(self):
        Helper.clear_screen()
        Helper.make_banner(f"{self.name}'s Stats")
        
        # Display enemy attributes
        print(f"HP: {self.chp}/{self.hp}")
        print(f"MP: {self.cmp}/{self.mp}")
        print(f"TP: {self.ctp}/{self.tp}")
        print(f"Constitution: {self.con}")
        print(f"Magic: {self.mag}")
        print(f"Strength: {self.str}")
        print(f"Intelligence: {self.int}")
        print(f"Dexterity: {self.dex}")
        print(f"Luck: {self.lck}")
        print(f"Physical Defense: {self.df}")
        print(f"Magical Defense: {self.mdf}")
        print()
        # Display equipped weapon details
        print(f"Equipped Weapon: {self.EQweapon.name}")

        # Display equipped armor details
        print(f"Equipped Armor: {self.EQarmor.name}")
        print()
        # Display equipped spell and skill details
        equipped_skills = [skill.name for skill in self.skills if skill is not None]
        equipped_spells = [spell.name for spell in self.spells if spell is not None]
        print(f"Prepaired Spells: {', '.join(equipped_spells)}")
        print(f"Prepaired Skills: {', '.join(equipped_skills)}")
        print()
        # Display status conditions
        status_conditions = []
        for condition in self.conditions:
            if condition:
                color = ''
                if condition.type == 'buff':
                    color = 'o'
                elif condition.type == 'debuff':
                    color = 'p'
                condition_info = f"{Helper.string_color(condition.name, color)} - {condition.duration} {condition.duration_type}"
                status_conditions.append(condition_info)
        print(f"Conditions: {', '.join(status_conditions)}\n")
        input()
    
    def get_atk(self):
        if self.EQweapon.stat == 'str':
            stat = self.get_str() * 2
        else:   #stat == dex
            stat = self.get_dex()
        atk = max(stat + randint(self.EQweapon.atkmin, self.EQweapon.atkmax), 1)
        if Helper.crit(self):
            print("Critical Hit!")
            atk = atk * 2
        return atk
    
    def get_df(self, atk):
        percentage_df = round(atk * (self.df / 100))
        total_defense = round((percentage_df + self.EQarmor.df ) * self.get_condition_multiplier('df'))
        return max(0, total_defense)  # Ensure the defense value doesn't drop below 0

    def get_matk(self, spell):
        matk = max(((self.get_mag() * 2) + randint(spell.matkmin, spell.matkmax) + randint(self.EQweapon.matkmin, self.EQweapon.matkmax)), 1)
        if Helper.crit(self):
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

    def get_action(self):
        """
        Determines and returns the action (skill or spell) the enemy should take.
        Returns None if we should just attack.
        """
        # Collect usable skills and spells based on resource costs
        skill_options = [skill for skill in self.skills if skill is not None and self.ctp >= skill.cost]
        spell_options = [spell for spell in self.spells if spell is not None and self.cmp >= spell.cost]

        # Determine whether to prefer skills or spells
        physical_score = self.str + self.dex
        magical_score = self.mag + self.int

        # Equal scores
        if physical_score == magical_score:
            if len(skill_options) > 0:
                return choice(skill_options)
            elif len(spell_options) > 0:
                return choice(spell_options)
            else:
                return None

        # Prefer physical actions
        if physical_score > magical_score and len(skill_options) > 0:
            return choice(skill_options)

        # Prefer magical actions
        if magical_score > physical_score and len(spell_options) > 0:
            return choice(spell_options)

        # Fallback if no options are available
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
                if condition.stat == 'hp':
                    if condition.type == 'debuff':
                        self.chp -= condition.multiplier
                        input(f"{self.name} took {Helper.string_color(condition.multiplier, 'r')} damage from {Helper.string_color(condition.name, 'p')}.")
                        if self.chp < 0:
                            self.chp = 0
                    elif condition.type == 'buff':
                        self.chp += condition.multiplier
                        input(f"{self.name} gained {Helper.string_color(condition.multiplier, 'r')} hp from {Helper.string_color(condition.name, 'o')}.")
                        if self.chp > self.hp:
                            self.chp = self.hp
                condition.duration -= 1
                if condition.duration == 0:
                    self.conditions.remove(condition)