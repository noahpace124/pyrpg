#Imports
from random import randint

#File Imports
from .weapons import Weapon
from .armors import Armor
from helper import Helper
from .crit import crit

#Class
class Player:
    def __init__(self, name, race, job, location):
        # Retrieve race and job instances
        self.race = race
        self.job = job

        #Calculations
        con = max(race.con, job.con)
        mag = max(race.mag, job.mag)
        str = max(race.str, job.str)
        int = max(race.int, job.int)
        dex = max(race.dex, job.dex)
        lck = max(race.lck, job.lck)
        lvl = con + mag + str + int + dex + lck
        hp = max(20 + ((con - 1) * 5), 1)
        mp = max(10 + ((int - 1) * 5), 0)
        tp = max(10 + ((dex - 1) * 5), 0)

        # Basic Information
        self.name = name
        self.lvl = lvl
        self.lvlnxt = self.lvl * 100
        self.xp = 0

        # Stats
        self.con = con
        self.mag = mag
        self.str = str
        self.int = int
        self.dex = dex
        self.lck = lck

        # Health and Mana
        self.hp = hp  
        self.chp = self.hp  
        self.mp = mp  
        self.cmp = self.mp  
        self.tp = tp 
        self.ctp = self.tp

        # Defense
        self.df = self.race.df
        self.mdf = self.race.mdf

        # Inventory and Equipment
        self.inv = [
            {'name': 'Lesser HP Potion', 'count': 3}, 
            {'name': 'Lesser MP Regen Potion', 'count': 3},
            {'name': self.job.weapon.name, 'count': 1},  # Add weapon to inventory
            {'name': self.job.armor.name, 'count': 1}    # Add armor to inventory
        ]
        self.EQweapon = self.job.weapon
        self.EQarmor = self.job.armor

        # Spells and Skills
        self.spells = self.job.spells
        self.EQspells = []
        if self.job.spells != []:
            for spell in self.job.spells:
                self.EQspells.append(spell)
        self.skills = self.job.skills
        self.EQskills = []
        if self.job.skills != []:
            for skill in self.job.skills:
                self.EQskills.append(skill)

        # Conditions, Location and Flags
        self.conditions = []
        self.gold = 0
        self.location = location
        self.flags = []

    def view_stats(self):
        Helper.clear_screen()
        Helper.make_banner(f"{self.name}'s Stats")
        print(f"Race: {self.race.name}")
        print(f"Class: {self.job.name}")
        
        # Display player attributes
        print(f"HP: {self.chp}/{self.hp}")
        print(f"MP: {self.cmp}/{self.mp}")
        print(f"TP: {self.ctp}/{self.tp}")
        print(f"XP: {self.lvlup}/{self.lvlnxt} LVL: {self.lvl}")
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
        equipped_spells = [spell.name for spell in self.EQspells]
        print(f"Prepaired Spells: {', '.join(equipped_spells)}")
        equipped_skills = [skill.name for skill in self.EQskills]
        print(f"Prepaired Skills: {', '.join(equipped_skills)}")

        # Display status conditions
        status_conditions = []
        for condition in self.conditions:
            condition_info = f"{condition.name}: {condition.duration} {condition.duration_type}"
            status_conditions.append(condition_info)
        print(f"Conditions: {', '.join(status_conditions)}\n")

        input("(Press enter to continue...) ")

    def equip_weapon(self, weapon):
        if weapon:
            if weapon.req1a:
                #weapon requirement 1 exists
                if getattr(self, weapon.req1a) >= weapon.req1m:
                    #meet weapon requirement 1
                    if weapon.req2a:
                        #weapon requirement 2 exists
                        if getattr(self, weapon.req2a) >= weapon.req2m:
                            #meet weapon requirement 2
                            self.EQweapon = weapon
                            input(f"{self.name} equipped {weapon.name}.")
                        else:
                            #don't meet weapon requirement 2
                            input(f"{self.name} does not meet the requirements to equip {weapon.name} ({weapon.req2a} {weapon.req2m})")
                    else:
                        #weapon requirement 2 doesn't exist and meet weapon requirement 1
                        self.EQweapon = weapon
                        input(f"{self.name} equipped {weapon.name}.")
                else:
                    #don't meet weapon requirement 1
                    input(f"{self.name} does not meet the requirements to equip {weapon.name} ({weapon.req1a} {weapon.req1m})")
            else:
                #no requirements for weapon
                self.EQweapon = weapon
                input(f"{self.name} equipped {weapon.name}.")
        else:  
            input(f"{self.name} cannot equip {weapon.name} because it was not found.")

    def equip_armor(self, armor):
        if armor:
            if armor.reqa:
                #armor requirement exists
                if getattr(self, armor.reqa) >= armor.reqm:
                    #meet armor requirement
                    self.EQarmor = armor
                    input(f"{self.name} equipped {armor.name}.")
                else:
                    #don't meet armor requirement
                    input(f"{self.name} does not meet the requirements to equip {armor.name} ({armor.reqa} {armor.reqm})")
            else:
                #no requirements for armor
                self.EQarmor = armor
                input(f"{self.name} equipped {armor.name}.")
        else:
            input(f"{self.name} cannot equip {armor.name} because it was not found.")
    
    def unequip_weapon(self, weapon):
        self.EQweapon = Weapon.get_weapon('None')
        input(f"{self.name} unequipped {weapon.name}.")
    
    def unequip_armor(self, armor):
        self.EQarmor = Armor.get_armor('None')
        input(f"{self.name} unequipped {armor.name}.")

    def equip_skill(self, skill):
        # Check if player meets skill requirements
        if getattr(self, skill.reqa) < skill.reqm:
            input(f"You do not meet the requirements to prepare {skill.name}.")
            return
        
        # Check if there's space for more equipped skills
        if max(round(self.dex / 3), 1) <= len(self.EQskills):
            input(f"You cannot prepare more skills until you increase your dexterity (DEX: {self.dex}).")
            return
        
        # Equip the skill
        self.EQskills.append(skill)
        input(f"{skill.name} has been prepared.")
    
    def unequip_skill(self, skill):
        self.EQskills.remove(skill)
        input(f"{skill.name} has been unprepared.")

    def equip_spell(self, spell):
        # Check if player meets spell requirements
        if self.int < spell.reqm:
            input(f"You do not meet the requirements to prepare {spell.name}.")
            return
        
        # Check if there's space for more equipped spells
        if max(round(self.int / 2), 1) <= len(self.EQspells):
            input(f"You cannot prepare more spells until you increase your intelligence (INT: {self.int}).")
            return
        
        # Equip the spell
        self.EQspells.append(spell)
        input(f"{spell.name} has been prepared.")

    def unequip_spell(self, spell):
        self.EQspells.remove(spell)
        input(f"{spell.name} has been unprepared.")

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

    def add_to_inventory(self, item):
        for inv_item in self.inv:
            if inv_item['name'] == item['name']:
                inv_item['count'] += item['count']  # Increase count for duplicates
                return
        self.inv.append(item)  # Add new item if it doesn't exist

    def remove_from_inventory(self, item_name, count=1):
        for inv_item in self.inv:
            if inv_item['name'] == item_name:
                if inv_item['count'] <= count:
                    self.inv.remove(inv_item)  # Remove item if count is zero
                else:
                    inv_item['count'] -= count  # Decrease count
                return

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