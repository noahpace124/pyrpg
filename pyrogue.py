#Imports from Packages

#Imports from Files
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
        else: #-1
            input("Invalid Answer: Try typing the letter or the name of the choice.")
    
    Helper.load_location(player)


#Execute
if __name__ == "__main__":
    main()