#Imports
import sys

from data.player import Player
from data.races import Race
from data.jobs import Job
from character_creation import character_creation
from helper import Helper

COMMANDS = [
    'New',
    'Load',
    'Exit'
]

#Functions
def main(): 
    while True:
        Helper.clear_screen()
        Helper.make_banner('PYRPG', True)
        
        print('New Game')
        print('Load Game')
        print('Exit')
        print()

        answer = Helper.handle_command(COMMANDS)

        if int(answer[0]) == 1:
            player = character_creation()
            break
        elif int(answer[0]) == 2:
            input("Loading game is not implemented yet.")
        elif int(answer[0]) == 3:
            exit()
    
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