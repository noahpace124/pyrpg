#Import
import random

#Import from File
from weapons import Weapon
from armors import Armor

class Enemy:
    def __init__(self, name, con, mag, str, int, dex, lck, df, mdf, weapon='None', armor='None', inv=[], spells=[], skills=[]):
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

        self.inv = inv
        self.EQweapon = weapon
        self.EQarmor = armor

        self.spells = spells
        self.skills = skills

        self.effects = []
    
    def __repr__(self):
        return (f"<Enemy(name={self.name}, "
                f"lvl={self.lvl}, HP={self.hp}, MP={self.mp}, TP={self.tp}, "
                f"con={self.con}, mag={self.mag}, str={self.str}, "
                f"int={self.int}, dex={self.dex}, lck={self.lck}, "
                f"df={self.df}, mdf={self.mdf})>")

    def get_weapon(self):
        if self.EQweapon:
            weapon = Weapon.get_weapon(self.EQweapon)
            return weapon if weapon else Weapon.get_weapon('None')
        return Weapon.get_weapon('None')

    def get_armor(self):
        if self.EQarmor:
            armor = Armor.get_armor(self.EQarmor)
            return armor if armor else Armor.get_armor('None')
        return Armor.get_armor('None')
    
    def get_atk(self):
        weapon = self.get_weapon()
        return (self.str * 2) + random.randint(weapon.atkmin, weapon.atkmax)
    
    def get_df(self, atk):
        armor = self.get_armor()
        # Calculate defense as a percentage of the enemy attack
        defense_from_self = atk * (self.df / 100)

        total_defense = defense_from_self + armor.df
        return max(0, round(total_defense))  # Ensure the defense value doesn't drop below 0