#Imports
from random import shuffle

from dungen import Dungeon
from data.dungeons.barrens import barrens_descriptions
from helper import Helper
from inventory import camp, inventory
from data.events import Event

#Functions
def run_events(player, num_rooms, events, location):
    #Get Descriptions based on location
    if location == "barrens":
        descriptions = barrens_descriptions

    dungeon = Dungeon(num_rooms, descriptions, events)

    room = dungeon.start

    while True:
        Helper.clear_screen()
        print(room.describe())
        input()

    # shuffle(events)
    # for event in events:
    #     Helper.clear_screen()
    #     event.func(player)

    #     while True:
    #         Helper.clear_screen()
    #         print("Do you want to access your inventory?")
    #         answer = Helper.yes_or_no()
    #         if answer == 1:
    #             inventory(player)
    #             break
    #         elif answer == 0:
    #             break

    # boss_events = Event.get_boss_events_by_location(location)
    # for e in boss_events:
    #     if e.flag in player.flags:
    #         return

    # Helper.clear_screen()
    # shuffle(boss_events)
    # event = boss_events[0]
    # event.func(player)
    # flag = f"{location} complete"
    # player.flags.append(flag)
    # Helper.clear_screen()
    # if event.flag in player.flags:
    #     return True
    # else:
    #     return False

def select_events(player, location):
    all_events = Event.get_events_by_location(location, player.flags)
    events = []
    while len(events) < 5:
        Helper.clear_screen()

        event_choices = []
        for event in all_events:
            if events.count(event) < event.max:
                event_choices.append(event)

        print("Choose your events: ")
        answer = Helper.prompt([f'{event.name}: {event.desc} (Count: {events.count(event)}/{event.max})' for event in event_choices])
        events.append(event_choices[answer])

    while True:
        Helper.clear_screen()
        events_print = []
        for event in events:
            if event.name not in [event['name'] for event in events_print]:
                events_print.append({'name': event.name, 'count': 1})
            else: #name in events_print:
                for e in events_print:
                    if e['name'] == event.name:
                        e['count'] += 1
                        break
        for event in events_print:
            print(f"{event['name']}: {event['count']}")
        print("Do you want venture out with these events?")
        answer = Helper.yes_or_no()
        if answer == 1: #yes
            return events
        elif answer == 0: #no
            return select_events(player, location)

#location functions
def barrens(player):
    camp(player)
    if "barrens complete" not in player.flags: #scripted first events
        Helper.clear_screen()
        print("As you approach the land of Zenith for the first time you end up in a dark and moutainous area.")
        print("It's hard to see without a light even in the daytime from the mysterious darkness here.")
        input("It would be rather easy to get lost or run into some unwanted company. Better be careful...")
        events = [Event.get_event("Goblin Encounter"), Event.get_event("Goblin Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Boulder")]
        if run_events(player, 5, events, 'barrens'): #beat the boss
            return #NEXT AREA
        else: #did not beat boss
            return barrens(player)
        
    else: #barrens complete
        events = select_events(player, 'barrens')
        if run_events(player, 5, events, 'barrens'): #beat the boss
            return #NEXT AREA
        else: #did not beat boss
            return barrens(player)