#Imports
import sys

from dungen import Dungeon
from helper import Helper
from inventory import camp, inventory
from data.events import Event


#Constants
COMMANDS = [
    "Help Commands",
    "Inventory",
    "View Look Room",
    "Interact",
    "North",
    "East",
    "South",
    "West"
]

#Functions
def run_events(player, events, location):
    dungeon = Dungeon(events, location)

    room = dungeon.start
    previous_room = None

    while True:
        Helper.clear_screen()
        result = room.visit(player)
        if result:
            if room.room_type == 'boss':
                break
            while True:
                answer = Helper.handle_command(COMMANDS)
                if int(answer[0]) == 0: #help
                    print("All commands:")
                    for command in COMMANDS:
                        print(command)
                elif int(answer[0]) == 1:
                    inventory(player)
                    break
                elif int(answer[0]) == 2: #look/view room
                    Helper.clear_screen()
                    print(room)
                elif int(answer[0]) == 3:
                    room.interact(player, answer)
                elif 4 <= int(answer[0]) <= 7: #direction
                    direction = COMMANDS[int(answer[0])].lower()
                    if room.connection_exists(direction):
                        previous_room = room
                        room = room.connections[direction]
                        break
                    else:
                        print(f"There is no path to the {direction}.")
        else: #ran/retreated
            room = previous_room
    input("Dungeon Complete")
    sys.exit()

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
        events = [Event.get_event("Goblin Encounter"), Event.get_event("Goblin Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Boulder"), Event.get_event("Goblin Shaman")]
        if run_events(player, events, 'barrens'): #beat the boss
            return #NEXT AREA
        else: #did not beat boss
            return barrens(player)
    # else:
    # TODO: Add event selection with dungeon
    # else: #barrens complete
    #     events = select_events(player, 'barrens')
    #     if run_events(player, 7, events, 'barrens'): #beat the boss
    #         return #NEXT AREA
    #     else: #did not beat boss
    #         return barrens(player)