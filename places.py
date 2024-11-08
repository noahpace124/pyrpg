#Imports
from random import shuffle

#Import from File
from helper import Helper
from inventory import camp, inventory
from data.events import Event

#Functions
def barrens(player):
    camp(player)
    Helper.clear_screen()
    if "barrens complete" not in player.flags:
        print("As you approach the land of Zenith for the first time you end up in a dark and moutainous area.")
        print("It's hard to see without a light even in the daytime from the mysterious darkness here.")
        print("It would be rather easy to get lost or run into some unwanted company. Better be careful...")
        input("(Press enter to continue...) ")
        events = [Event.get_event("Goblin Encounter"), Event.get_event("Goblin Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Boulder")]
        shuffle(events)
        for event in events:
            Helper.clear_screen()
            event.func(player)
            while True:
                Helper.clear_screen()
                print("Do you want to access your inventory?")
                ans = input(">> ")
                if Helper.yes_or_no(ans) == 1:
                    inventory(player)
                    break
                elif Helper.yes_or_no(ans) == 0:
                    break
                else:
                    input("Invalid answer. Try typing 'yes' or 'no'.")


