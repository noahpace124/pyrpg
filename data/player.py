#Imports
from random import randint

#File Imports
from .weapons import Weapon
from .armors import Armor
from helper import Helper

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
        hp = 20 + ((con - 1) * 5)
        mp = 10 + ((int - 1) * 5) 
        tp = 10 + ((dex - 1) * 5)

        # Basic Information
        self.name = name
        self.lvl = lvl
        self.lvlnxt = self.lvl * 5
        self.lvlup = 0

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
        for spell in self.job.spells:
            self.EQspells.append(spell)
        self.skills = self.job.skills
        self.EQskills = []
        for skill in self.job.skills:
            self.EQskills.append(skill)

        # Effects and Other Properties
        self.effects = []
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

        # Dislay equipped spell and skill details
        equipped_spells = [spell.name for spell in self.EQspells]
        print(f"Prepaired Spells: {', '.join(equipped_spells)}")
        equipped_skills = [skill.name for skill in self.EQskills]
        print(f"Prepaired Skills: {', '.join(equipped_skills)}\n")

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
            print(f"You do not meet the requirements to prepare {spell.name}.")
            return
        
        # Check if there's space for more equipped spells
        if max(round(self.int / 2), 1) <= len(self.EQspells):
            print(f"You cannot prepare more spells until you increase your intelligence (INT: {self.int}).")
            return
        
        # Equip the spell
        self.EQspells.append(spell)
        print(f"{spell.name} has been prepared.")

    def unequip_spell(self, spell):
        self.EQspells.remove(spell)
        input(f"{spell.name} has been unprepared.")

    def get_atk(self):
        return (self.str * 2) + randint(self.EQweapon.atkmin, self.EQweapon.atkmax)
    
    def get_df(self, atk):
        percentage_df = round(atk * (self.df / 100))

        total_defense = percentage_df + self.EQarmor.df
        return max(0, total_defense)  # Ensure the defense value doesn't drop below 0
    
    def get_matk(self, spell):
        return (self.mag * 2) + randint(spell.matkmin, spell.matkmax) + randint(self.EQweapon.matkmin, self.EQweapon.matkmax)

    def get_mdf(self, ematk):
        percentage_mdf = round((ematk * (self.mdf / 100)))
        return percentage_mdf + self.EQarmor.mdf

    def get_spd(self):
        return (self.dex * 2) + max(0, self.lck)

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

    def regen(self):
        self.ctp += self.dex
        if self.ctp > self.tp:
            self.ctp = self.tp
        self.cmp += self.int
        if self.cmp > self.mp:
            self.cmp = self.mp