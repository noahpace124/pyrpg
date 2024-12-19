#Imports
import sys

from character_creation import character_creation
from helper import Helper

#Functions
def main(): 
    while True:
        Helper.clear_screen()
        Helper.make_banner('PYRPG', True)

        choices = ["New Game", "Load Game", "Exit"]

        answer = Helper.prompt(choices)

        if answer == 0:
            player = character_creation()
            break
        elif answer == 1:
            print("Load what character? ")
            name = input(">> ")
            if len(name.strip()) == 0:
                input("Invalid Name: Name must be made of characters.")
                continue
            player = Helper.load(name)
            break
        elif answer == 2:
            exit()
    
    Helper.load_location(player)

def debug(): #for debugging
    return

#Execute
if __name__ == "__main__":
    if "--debug" in sys.argv:
        debug()
    else: 
        main()