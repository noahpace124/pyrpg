#Imports
import random

#File Imports
from .weapons import Weapon
from .armors import Armor

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
            {'name': self.job.weapon, 'count': 1},  # Add weapon to inventory
            {'name': self.job.armor, 'count': 1}    # Add armor to inventory
        ]
        self.EQweapon = self.job.weapon
        self.EQarmor = self.job.armor
        self.EQspells = []
        self.spells = self.job.spells
        # for spell in self.job.spells:
        #     self.equip_spell(spell.name)
        self.EQskills = []
        self.skills = self.job.skills
        # for skill in self.job.skills:
        #     self.equip_skill(skill.name)

        # Effects and Other Properties
        self.effects = []
        self.location = location
        self.flags = []

    def __repr__(self):
        return (f"<Player(name={self.name}, race={self.race}, job={self.job}, "
                f"lvl={self.lvl}, HP={self.hp}, MP={self.mp}, TP={self.tp}, "
                f"con={self.con}, mag={self.mag}, str={self.str}, "
                f"int={self.int}, dex={self.dex}, lck={self.lck}, "
                f"df={self.df}, mdf={self.mdf})>")

    def equip_weapon(self, weapon_name):
        weapon = Weapon.get_weapon(weapon_name)
        if weapon:
            if weapon.req1a:
                #weapon requirement 1 exists
                if getattr(self, weapon.req1a) >= weapon.req1m:
                    #meet weapon requirement 1
                    if weapon.req2a:
                        #weapon requirement 2 exists
                        if getattr(self, weapon.req2a) >= weapon.req2m:
                            #meet weapon requirement 2
                            self.EQweapon = weapon.name
                            print(f"{self.name} equipped {weapon.name}.")
                        else:
                            #don't meet weapon requirement 2
                            print(f"{self.name} does not meet the requirements to equip {weapon.name} ({weapon.req2a} {weapon.req2m})")
                    else:
                        #weapon requirement 2 doesn't exist and meet weapon requirement 1
                        self.EQweapon = weapon.name
                        print(f"{self.name} equipped {weapon.name}.")
                else:
                    #don't meet weapon requirement 1
                    print(f"{self.name} does not meet the requirements to equip {weapon.name} ({weapon.req1a} {weapon.req1m})")
            else:
                #no requirements for weapon
                self.EQweapon = weapon.name
                print(f"{self.name} equipped {weapon.name}.")
        else:  
            print(f"{self.name} cannot equip {weapon.name} because it was not found.")
        input("(Press enter to continue...) ")

    def equip_armor(self, armor_name):
        armor = Armor.get_armor(armor_name)
        if armor:
            if armor.reqa:
                #armor requirement exists
                if getattr(self, armor.reqa) >= armor.reqm:
                    #meet armor requirement
                    self.EQarmor = armor.name
                    print(f"{self.name} equipped {armor.name}.")
                else:
                    #don't meet armor requirement
                    print(f"{self.name} does not meet the requirements to equip {armor.name} ({armor.reqa} {armor.reqm})")
            else:
                #no requirements for armor
                self.EQarmor = armor.name
                print(f"{self.name} equipped {armor.name}.")
        else:
            print(f"{self.name} cannot equip {armor_name} because it was not found.")
        input("(Press enter to continue...) ")
        
    def get_weapon(self):
        if self.EQweapon:
            weapon = Weapon.get_weapon(self.EQweapon)
            return weapon if weapon else Weapon.get_weapon('None')
        return Weapon.get_weapon('None')
    
    def unequip_weapon(self, weapon_name):
        self.EQweapon = 'None'
        print(f"{self.name} unequipped {weapon_name}.")
        input("(Press enter to continue...) ")

    def get_armor(self):
        if self.EQarmor:
            armor = Armor.get_armor(self.EQarmor)
            return armor if armor else Armor.get_armor('None')
        return Armor.get_armor('None')
    
    def unequip_armor(self, armor_name):
        self.EQarmor = 'None'
        print(f"{self.name} unequipped {armor_name}.")
        input("(Press enter to continue...) ")

    # def equip_skill(self, skill_name):
    #     skill = Skill.get_skill(skill_name)
        
    #     # Check if player meets skill requirements
    #     if getattr(self, skill.reqa) < skill.reqm:
    #         print(f"You do not meet the requirements to equip {skill.name}.")
    #         return
        
    #     # Check if there's space for more equipped skills
    #     if len(self.EQskills) >= self.dex:
    #         print(f"You cannot equip more skills unless you increase your dexterity (DEX: {self.dex}).")
    #         return
        
    #     # Equip the skill
    #     self.EQskills.append(skill)
    #     print(f"{skill.name} has been equipped.")
    
    # def unequip_skill(self, skill_name):
    #     skill = Skill.get_skill(skill_name)
    #     self.EQskills.remove(skill)
    #     print(f"{skill.name} has been unequipped.")

    # def equip_spell(self, spell_name):
    #     spell = Spell.get_spell(spell_name)

    #     # Check if player meets spell requirements
    #     if self.int < spell.reqm:
    #         print(f"You do not meet the requirements to equip {spell.name}.")
    #         return
        
    #     # Check if there's space for more equipped spells
    #     if len(self.EQspells) >= self.int:
    #         print(f"You cannot equip more skills unless you increase your intelligence (INT: {self.int}).")
    #         return
        
    #     # Equip the spell
    #     self.EQspells.append(spell)
    #     print(f"{spell.name} has been equipped.")

    # def unequip_spell(self, spell_name):
    #     spell = Spell.get_spell(spell_name)
    #     self.EQspells.remove(spell)
    #     print(f"{spell.name} has been unequipped.")

    def get_atk(self):
        weapon = self.get_weapon()
        return (self.str * 2) + random.randint(weapon.atkmin, weapon.atkmax)
    
    def get_df(self, atk):
        armor = self.get_armor()
        # Calculate defense as a percentage of the enemy attack
        defense_from_self = atk * (self.df / 100)

        total_defense = defense_from_self + armor.df
        return max(0, round(total_defense))  # Ensure the defense value doesn't drop below 0
    
    # def get_matk(self, spell_name):
    #     spell = Spell.get_spell(spell_name)  # Now calls the class method
    #     if spell is None:
    #         print(f"Spell {spell_name} not found.")
    #         return 0

    #     if self.cmp < spell.cost:  # Check if the player has enough mana to cast the spell
    #         print(f"Not enough mana to cast {spell.name}.")
    #         return 0  # or you could raise an exception depending on your design

    #     self.cmp -= spell.cost  # Deduct the mana cost
    #     weapon = self.get_weapon()  # Get the player's equipped weapon

    #     # Calculate magic attack
    #     matk = (self.mag * 2) + random.randint(spell.matkmin, spell.matkmax) + random.randint(weapon.matkmin, weapon.matkmax)
    #     return matk

    # def get_mdf(self, ematk):
    #     armor = self.getArmor()
    #     # Calculate the magical defense based on a percentage of the enemy's magical attack
    #     percentage_defense = ematk * (self.mdf / 100)
    #     return round(percentage_defense) + armor['mdf']

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
