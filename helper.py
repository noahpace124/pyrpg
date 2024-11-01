#Imports
import os
import platform

#Import from File

class Helper:
    @staticmethod
    def clear_screen():
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def yes_or_no(ans):
        ans = ans.replace(" ", "")
        if ans == 'y' or ans == 'ye' or ans == 'yes':
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
            print(f" - - - {banner} - - -")

    @staticmethod
    def load_location(player):
        if player.location == "barrens":
            from places import barrens
            return barrens(player)
