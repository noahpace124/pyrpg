#Imports
import os
import platform
import string
from itertools import product
from random import randint

#Costants
BAR_LENGTH = 14

# ANSI color codes
COLORS = {
    "green": "\033[32m",
    "yellow": "\033[33m",
    "red": "\033[31m",
    "dark_green": "\033[38;5;22m",
    "blue": "\033[34m",
    "purple": "\033[38;5;13m",
    "orange": "\033[38;5;214m",
    "reset": "\033[0m"
}

class Helper:
    @staticmethod
    def clear_screen():
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def prompt(choices):
        #create labels for choice
        label_generator = generate_labels()

        #create array for each choice
        choice_array = [f"{next(label_generator)}) {choice}" for choice in choices]
        for choice in choice_array:
            print(choice)

        while True:
            # Input handling
            answer = input(">> ").strip().lower()
            for i, choice in enumerate(choice_array):
                label, text = choice.split(') ', maxsplit=1)
                text_lower = text.lower()
                # Match by label or exact/starting text match
                if answer == label or answer == text_lower or text_lower.startswith(answer):
                    return i

            print("Invalid Answer: Try typing the option or the name of the choice.")

    @staticmethod
    def yes_or_no():
        while True:
            ans  = input('>> ').lower().strip()
            if ans == 'y' or ans == 'ye' or ans == 'es' or ans == 'ys' or ans == 'yes':
                return 1
            elif ans == 'n' or ans == 'no':
                return 0
            else:
                print("Invalid Answer: Try typing yes or no.")
    
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
    def string_color(string, color):
        if color == '':
            string_color = COLORS['reset']
        elif color == 'r':
            string_color = COLORS['red']
        elif color == 'y':
            string_color = COLORS['yellow']
        elif color == 'p':
            string_color = COLORS['purple']
        elif color == 'o':
            string_color = COLORS['orange']

        return f"{string_color}{string}{COLORS['reset']}"

    @staticmethod
    def render_hp_bar(current_value, max_value):
        # Calculate the filled length of the bar
        filled_length = int(BAR_LENGTH * current_value // max_value)

        # Select the color based on the current value
        if current_value / max_value <= 0.25:
            bar_color = COLORS["red"]
            hp_color = COLORS["yellow"]
        elif current_value / max_value <= 0.5:
            bar_color = COLORS["yellow"]
            hp_color = COLORS["yellow"]
        else:
            bar_color = COLORS["green"]
            hp_color = COLORS["reset"]

        # Create the bar
        bar = "█" * filled_length + " " * (BAR_LENGTH - filled_length)

        # Return the result
        return f"[{bar_color}{bar}{COLORS['reset']}] {hp_color}{current_value}{COLORS['reset']}/{max_value}"
    
    @staticmethod
    def render_bar(current_value, max_value, color):
        if color == 'dg':
            bar_color = COLORS['dark_green']
        elif color == 'b':
            bar_color = COLORS['blue']
        elif color == 'r':
            bar_color = COLORS['red']

        # Calculate the filled length of the bar
        filled_length = int(14 * current_value // max_value)

        # Select the color based on the current value
        if current_value / max_value <= 0.25:
            value_color = COLORS["red"]
        elif current_value / max_value <= 0.5:
            value_color = COLORS["yellow"]
        else:
            value_color = COLORS["reset"]

        # Create the bar
        bar = "█" * filled_length + " " * (BAR_LENGTH - filled_length)

        # Return the result
        return f"[{bar_color}{bar}{COLORS['reset']}] {value_color}{current_value}{COLORS['reset']}/{max_value} "
    
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
            print(f"What stat do you want to increase? (Stat Points Remaining: {points})")
            answer = Helper.prompt(['Constitution', 'Magic', 'Strength', 'Intelligence', 'Dexterity', 'Luck'])
            if answer == 0:
                player.con += 1
                player.hp = 20 + ((player.con - 1) * 5)
            if answer == 1:
                player.mag += 1
            if answer == 2:
                player.str += 1
            if answer == 3:
                player.int += 1
                player.mp = 10 + ((player.int - 1) * 5)
            if answer == 4:
                player.dex += 1
                player.tp = 10 + ((player.dex - 1) * 5)
            if answer == 5:
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


def generate_labels():
    """Generate labels like 'a', 'b', ..., 'z', 'aa', 'ab', ..."""
    alphabet = string.ascii_lowercase
    length = 1
    while True:
        for letters in product(alphabet, repeat=length):
            yield ''.join(letters)
        length += 1