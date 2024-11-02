#Imports

#Import from File
from helper import Helper
from inventory import camp
from data.events import Event

#Functions
def barrens(player):
    camp(player)
    Helper.clear_screen()
    print("As you approach the land of Zenith for the first time you end up in a dark and moutainous area.")
    print("It's hard to see without a light even in the daytime from the mysterious darkness here.")
    print("It would be rather easy to get lost or run into some unwanted company. Better be careful...")
    input("(Press enter to continue...) ")
    events = [Event.get_event("Goblin Encounter")]
    for event in events:
        event.func(player)
    print("MADE IT TO THE END")

