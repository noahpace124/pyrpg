#Imports
from random import shuffle

from helper import Helper
from inventory import camp, inventory
from data.events import Event

#Functions
def barrens(player):
    camp(player)
    if "barrens complete" not in player.flags:
        Helper.clear_screen()
        print("As you approach the land of Zenith for the first time you end up in a dark and moutainous area.")
        print("It's hard to see without a light even in the daytime from the mysterious darkness here.")
        input("It would be rather easy to get lost or run into some unwanted company. Better be careful...")
        events = [Event.get_event("Goblin Encounter"), Event.get_event("Goblin Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Boulder")]
        shuffle(events)
        for event in events:
            Helper.clear_screen()
            event.func(player)
            while True:
                Helper.clear_screen()
                print("Do you want to access your inventory?")
                answer = Helper.yes_or_no()
                if answer == 1:
                    inventory(player)
                    break
                elif answer == 0:
                    break
        Helper.clear_screen()
        event = Event.get_event("Goblin Shaman")  
        event.func(player)
        Helper.clear_screen()
        if 'barrens boss' in player.flags:
            input(f"You beat the game for now, but you can continue if you wish.")
            return barrens(player) #REPLACE WITH NEW LOCATION
        else: #ran away from boss
            return barrens(player)
        
    else: #barrens complete
        event_choices = Event.get_events_by_location('barrens', player.flags)
        events = []
        while len(events) < 5:
            Helper.clear_screen()

            print("Choose your events: ")
            answer = Helper.prompt([f'{event.name}: {event.desc} (Count: {events.count(event)}/{event.max})' for event in event_choices])
            chosen_event_name = answer['selected_event'].split(':')[0].strip()
            event = Event.get_event(chosen_event_name)

            if events.count(event) < event.max:
                events.append(event)
            else:
                input(f"You already have the most of this event possible. (Count: {events.count(event)}/{event.max})")

        while True:
            Helper.clear_screen()
            print("Your events:")
            for event in events: print(f"   {event.name}: {event.desc}")
            print("Do you want venture out with these events?")
            answer = Helper.yes_or_no()
            if answer == 1: #yes
                break
            elif answer == 0: #no
                return barrens(player)
        shuffle(events)
        for event in events:
            Helper.clear_screen()
            event.func(player)

            while True:
                Helper.clear_screen()
                print("Do you want to access your inventory?")
                answer = Helper.yes_or_no()
                if answer == 1:
                    inventory(player)
                    break
                elif answer == 0:
                    break

        if 'barrens boss' not in player.flags:
            Helper.clear_screen()
            event = Event.get_event("Goblin Shaman")  
            event.func(player)
            Helper.clear_screen()
            if 'barrens boss' in player.flags:
                return barrens(player) #REPLACE WITH NEW LOCATION
            else: #did not beat boss
                return barrens(player)