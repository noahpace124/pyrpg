#Imports
import os
import platform
import inquirer
import string
from random import randint

#Import from File

class Helper:
    @staticmethod
    def clear_screen():
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def prompt(choices):
        choice_array = []
        i = 0
        alphabet = string.ascii_lowercase
        for choice in choices:
            choice_array.append(f"{alphabet[i]}) {choice}")
            i += 1
        for choice in choice_array:
            print(choice)
        answer = input(">> ").lower()
        i = 0
        for choice in choice_array:
            temp = choice.split(') ')
            if len(answer.strip()) == 1 and answer.strip() == temp[0]:
                return i
            if answer in temp[1].lower():
                return i
            i += 1
        return -1 #If we get here no answer was selected correctly

    @staticmethod
    def yes_or_no():
        ans  = input('>> ')
        ans = ans.lower().strip()
        if ans == 'y' or ans == 'ye' or ans == 'es' or ans == 'ys' or ans == 'yes':
            return 1
        elif ans == 'n' or ans == 'no':
            return 0
        else:
            return -1
    
    @staticmethod
    def make_banner(banner, spaces=False):
        if spaces == False:
            print(f" - - - {banner} - - -")
        else:
            spaced = ' '.join(banner)
            print(f" - - - {spaced} - - -")

    @staticmethod
    def load_location(player):
        if player.location == "barrens":
            from places import barrens
            return barrens(player)
    
    @staticmethod
    def award_xp(player, xp):
        print()
        input(f"{player.name} gained {xp} experience.")
        print()
        player.xp += xp
        points = 0
        while player.xp > player.lvlnxt:
            player.xp -= player.lvlnxt
            player.lvl += 1
            player.lvlnxt = 100 + (player.lvl * 100)
            points += 1
            input(f"{player.name} leveled up to level {player.lvl}!")
        while points > 0:
            print()
            questions = [
                inquirer.List('choice',
                            message=f"What stat do you want to increase? (Stat Points Remaining: {points})",
                            choices=['Constitution', 'Magic', 'Strength', 'Intelligence', 'Dexterity', 'Luck'],
                            ),
            ]
            answer = inquirer.prompt(questions)
            stat = answer['choice']
            if stat == 'Constitution':
                player.con += 1
                player.hp = 20 + ((player.con - 1) * 5)
            if stat == 'Magic':
                player.mag += 1
            if stat == 'Strength':
                player.str += 1
            if stat == 'Intelligence':
                player.int += 1
                player.mp = 10 + ((player.int - 1) * 5)
            if stat == 'Dexterity':
                player.dex += 1
                player.tp = 10 + ((player.dex - 1) * 5)
            if stat == 'Luck':
                player.lck += 1
            player.chp = player.hp
            player.cmp = player.mp
            player.ctp = player.tp
            points -= 1
            print()

    @staticmethod        
    def crit(attacker):
        if randint(1, 100) <= attacker.get_lck():
            return True
        else:
            return False
        