#Imports
from random import choice

from data.dungeons.barrens import barrens_descriptions
from data.items import Item
from data.weapons import Weapon
from data.armors import Armor
from dungen import Dungeon
from helper import Helper
from inventory import camp, inventory
from data.events import Event

#Functions
def run_events(player, events, location):
    if location == "barrens":
        descriptions = barrens_descriptions

    dungeon = Dungeon(events, descriptions, location)

    room = dungeon.start
    previous_room = None

    while True:
        Helper.clear_screen()
        result = room.visit(player)
        if result:
            if room.room_type == 'boss':
                break
            while True:
                answer = Helper.handle_commands("places")
                
                if answer.name == "Use":
                    for inv_item in player.inv:
                        if answer.vals in inv_item["name"].lower():
                            item_name = inv_item["name"]                    
                        item = Item.get_item(item_name)
                    if item:
                        if item.can_use(player):
                            item.func(player)
                    else:
                        input(f"{player.name} cannot use the {answer.vals} because it isn't a consumable.")
                elif answer.name == "View":
                    for inv_item in player.inv:
                        if answer.vals in inv_item["name"].lower():
                            item_name = inv_item["name"]
                    if isinstance(Weapon.get_weapon(item_name), Weapon):
                        weapon = Weapon.get_weapon(item_name)
                        Helper.make_banner(f"{weapon.name}")
                        print(f"Description: {weapon.desc}")
                        for item in player.inv:
                            if isinstance(Weapon.get_weapon(item['name']), Weapon):
                                print(f"Count: {item['count']}")
                        print(f"Attack: {weapon.atkmin} to {weapon.atkmax}")
                        print(f"Magic Attack: {weapon.matkmin} to {weapon.matkmax}")
                        if weapon.req1a:
                            print(f"Requirements: {weapon.req1a.upper()}: {weapon.req1m}")
                            if weapon.req2a:
                                print(f"              {weapon.req2a.upper()}: {weapon.req2m}")
                        input()
                    elif isinstance(Armor.get_armor(item_name), Armor):
                        armor = Armor.get_armor(item_name)
                        # Display armor details
                        Helper.make_banner(f"{armor.name}")
                        print(f"Description: {armor.desc}")
                        for item in player.inv:
                            if isinstance(Armor.get_armor(item['name']), Armor):
                                print(f"Count: {item['count']}")
                        print(f"Defense: {armor.df}")
                        print(f"Magic Defense: {armor.mdf}")
                        if armor.reqa:
                            print(f"Requires: {armor.reqa.upper()}: {armor.reqm}")
                        input()
                    elif isinstance(Item.get_item(item_name), Item):
                        item = Item.get_item(item_name)
                        # Display item details
                        Helper.make_banner(f"{item.name}")
                        print(f"Description: {item.desc}")
                        input()
                    else: #not a valid item
                        input(f"{player.name} cannot look at the {item_name} because it doesn't exist.") 
                elif answer.name == "Inventory":
                    inventory(player)
                    break
                elif answer.name == "Look":
                    Helper.clear_screen()
                    print(room)
                elif answer.name == "Go":
                    direction = answer.vals
                    if room.connection_exists(direction):
                        previous_room = room
                        room = room.connections[direction]
                        break
                    else:
                        print(f"There is no path to the {direction}.")
                else: #Check
                    room.interact(player, answer.vals)
                    Helper.clear_screen()
        else: #ran/retreated
            room = previous_room

def select_events(player, location):
    all_events = Event.get_events_by_location(location, player.flags)

    if location == "barrens":
        descriptions = barrens_descriptions
        
    events = []
    
    boss_events = []
    for event in all_events:
        if event.flag:
            if 'boss' in event.flag:
                boss_events.append(event)
    if not boss_events: #no boss event in options, add a random boss event by location
        events.append(choice(Event.get_boss_events_by_location(location)))

    if boss_events: #boss option
        factor = 1
        min = 6
    else:
        factor = 2
        min = 5

    while len(events) <= len(descriptions) - factor:
        Helper.clear_screen()

        event_choices = []
        for event in all_events:
            if events.count(event) < event.max:
                event_choices.append(event)

        if boss_events: #boss option
            print(f"{len(events)}/{len(descriptions) - factor} (Minimum: {min} with boss event)") #-1 for the starting room
        else:
            print(f"{len(events) - 1}/{len(descriptions) - factor} (Minimum: {min})") #-1 for boss event, -2 for the starting room and boss event
        print("Choose your events: ")
        choices = [f'{event.name}: {event.desc} (Count: {events.count(event)}/{event.max})' for event in event_choices]
        choices.append('Random Events')
        choices.append('Finish')
        answer = Helper.prompt(choices)
        if answer == (len(choices) - 1): #Finish
            if len(events) >= min:
                temp = []
                for event in events:
                    if event.flag:
                        if 'boss' in event.flag:
                            temp.append(event)
                if not temp: #no boss event in our choices
                    input(f"You need a boss event!")
                else:
                    break
            else: #not enough events
                input(f"You need at least {min} events!")
        elif answer == (len(choices) - 2): #Random Events
            events = generate_random_events(player, location)
            break
        else:
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

def generate_random_events(player, location):
    events = []
    all_events = Event.get_events_by_location(location, player.flags)

    boss_events = []
    for event in all_events:
        if event.flag:
            if 'boss' in event.flag:
                boss_events.append(event)
                all_events.remove(event)
    
    while len(events) < 5:
        events.append(choice(all_events))
    
    if not boss_events: #no boss event in options, add a random boss event by location
        events.append(choice(Event.get_boss_events_by_location(location)))
    else:
        events.append(choice(boss_events))

    return events

#location functions
def barrens(player):
    camp(player)
    if "barrens complete" not in player.flags: #scripted first events
        Helper.clear_screen()
        print("As you approach the land of Zenith for the first time you end up in a dark and moutainous area.")
        print("It's hard to see without a light even in the daytime from the mysterious darkness here.")
        input("It would be rather easy to get lost or run into some unwanted company. Better be careful...")
        events = [Event.get_event("Goblin Encounter"), Event.get_event("Goblin Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Kobold Encounter"), Event.get_event("Boulder"), Event.get_event("Goblin Shaman")]
        if run_events(player, events,'barrens'): #beat the boss
            return #NEXT AREA
        else: #did not beat boss
            return barrens(player)
    else: #barrens complete
        events = select_events(player, 'barrens')
        if run_events(player, events, 'barrens'): #beat the boss
            return #NEXT AREA
        else: #did not beat boss
            return barrens(player)