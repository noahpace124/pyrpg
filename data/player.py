#Imports
from random import randint

from .weapons import Weapon
from .armors import Armor
from helper import Helper

#Class
class Player:
    def __init__(self, name, race, job, location, flags=None):
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
        hp = 20 + (5 * con)
        mp = int * 5
        tp = dex * 5

        # Basic Information
        self.name = name
        self.lvl = lvl
        self.lvlnxt = 100 + (self.lvl * 100)
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
        self.flags = flags if flags else []

    def view_stats(self):
        Helper.clear_screen()
        Helper.make_banner(f"{self.name}'s Stats")
        print(f"Race: {self.race.name}")
        print(f"Class: {self.job.name}")
        print()
        # Display player attributes
        print(f"HP: {self.chp}/{self.hp}")
        print(f"MP: {self.cmp}/{self.mp}")
        print(f"TP: {self.ctp}/{self.tp}")
        print(f"XP: {self.xp}/{self.lvlnxt} LVL: {self.lvl}")
        print(f"Gold: {self.gold}")
        print(f"Strength: {self.str}")
        print(f"Constitution: {self.con}")
        print(f"Magic: {self.mag}")
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
        equipped_spells = [spell.name for spell in self.EQspells]
        print(f"Prepaired Spells: {', '.join(equipped_spells)}")
        equipped_skills = [skill.name for skill in self.EQskills]
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
        input("")

    def equip(self, item):
        item_name = item
        for inv_item in self.inv:
            if item in inv_item["name"].lower():
                item_name = inv_item["name"]
        if isinstance(Weapon.get_weapon(item_name), Weapon):
            weapon = Weapon.get_weapon(item_name)
            if self.EQweapon == weapon:
                input(f"{self.name} already has the {weapon.name} equipped!")
                return
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
        elif isinstance(Armor.get_armor(item_name), Armor):
            armor = Armor.get_armor(item_name)
            if self.EQarmor == armor:
                input(f"{self.name} alread has the {armor.name} equipped!")
                return
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
            input(f"{self.name} cannot equip {item} because it isn't equippable.")
    
    def unequip(self, item):
        item_name = item
        for inv_item in self.inv:
            if item in inv_item["name"].lower():
                item_name = inv_item["name"]
        if isinstance(Weapon.get_weapon(item_name), Weapon):
            self.EQweapon = Weapon.get_weapon('None')
            input(f"{self.name} unequipped {item_name}.")
        elif isinstance(Armor.get_armor(item_name), Armor):
            self.EQarmor = Armor.get_armor('None')
            input(f"{self.name} unequipped {item_name}.")
        else:
            input(f"{self.name} cannot unequip {item} because it isn't unequippable.")

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
        multiplier = self.get_condition_multiplier('str')
        adder = self.get_condition_adder('str')
        return round((self.str + adder) * multiplier)

    def get_dex(self):
        multiplier = self.get_condition_multiplier('dex')
        adder = self.get_condition_adder('dex')
        return round((self.dex + adder) * multiplier)

    def get_mag(self):
        multiplier = self.get_condition_multiplier('mag')
        adder = self.get_condition_adder('mag')
        return round((self.mag + adder) * multiplier)

    def get_int(self):
        multiplier = self.get_condition_multiplier('int')
        adder = self.get_condition_adder('int')
        return round((self.int + adder) * multiplier)

    def get_lck(self):
        multiplier = self.get_condition_multiplier('lck')
        adder = self.get_condition_adder('lck')
        return round((self.lck + adder) * multiplier)

    def get_spd(self):
        return max((self.get_dex() * 2) + max(0, self.get_lck()), 0)

    def get_condition_multiplier(self, stat):
        multiplier = 1
        for condition in self.conditions:
            if condition:
                if condition.modification == '*':
                    if condition.stat == stat:
                        multiplier *= condition.modifier
        return multiplier
    
    def get_condition_adder(self, stat):
        adder = 0
        for condition in self.conditions:
            if condition:
                if condition.modification == '+':
                    if condition.stat == stat:
                        adder += condition.modifier
        return adder

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
                if condition.stat == 'hp':
                    if condition.type == 'debuff':
                        hp_loss = 0
                        if condition.modification == '*':
                            hp_loss = round(condition.modifier * self.hp)
                            self.chp -= hp_loss
                        elif condition.modification == '+':
                            hp_loss = condition.modifier
                            self.chp -= hp_loss
                        input(f"{self.name} took {Helper.string_color(hp_loss, 'r')} damage from {Helper.string_color(condition.name, 'p')}.")
                        if self.chp < 0:
                            self.chp = 0
                    elif condition.type == 'buff':
                        hp_gain = 0
                        if condition.modification == '*':
                            hp_gain = round(condition.modifier * self.hp)
                            self.chp += hp_gain
                        elif condition.modification == '+':
                            hp_gain = condition.modifier
                            self.chp += hp_gain
                        input(f"{self.name} gained {Helper.string_color(hp_gain, 'g')} hp from {Helper.string_color(condition.name, 'o')}.")
                        if self.chp > self.hp:
                            self.chp = self.hp
                condition.duration -= 1
                if condition.duration == 0:
                    self.conditions.remove(condition)