#Imports
import sys

from data.player import Player
from data.races import Race
from data.jobs import Job
from character_creation import character_creation
from helper import Helper

#Functions
def main(): 
    while True:
        Helper.clear_screen()
        Helper.make_banner('PYROGUE', True)

        answer = Helper.prompt(['New Game', 'Load Game', 'Exit'])

        if answer == 0:
            player = character_creation()
            break
        elif answer == 1:
            input("Loading game is not implemented yet.")
        elif answer == 2:
            exit()
        input(answer)
    
    Helper.load_location(player)

def debug():
    player = Player("Ralsei", Race.get_race("Xeran"), Job.get_job("Wizard"), 'barrens')
    Helper.load_location(player)


#Execute
if __name__ == "__main__":
    if "--debug" in sys.argv:
        debug()
    else: 
        main()