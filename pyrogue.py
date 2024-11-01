#Imports from Packages
import os
import inquirer

#Imports from Files
from character_creation import character_creation
from helper import Helper

#Functions
def title_screen():
    while True:
        Helper.clear_screen()
        Helper.make_banner('PYROGUE', True)

        questions = [
            inquirer.List('choice',
                        message="Please select an option",
                        choices=["New Game", "Load Game", "DEBUG", "Exit"],
                        ),
        ]

        answer = inquirer.prompt(questions)

        if answer['choice'] == 'New Game':
            player = character_creation()
            break
        elif answer['choice'] == 'Load Game':
            print("Loading game is not implemented yet.")
            input("(Press enter to continue...) ")
        elif answer['choice'] == 'Exit':
            exit()
    
    Helper.load_location(player)

def main(): 
    title_screen()


#Execute
if __name__ == "__main__":
    main()