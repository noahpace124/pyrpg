#Imports
from random import shuffle, choice, randint

from helper import Helper, match_count
from data.dungeons.barrens import barrens_descriptions
from data.interactables import Interactable

class Room:
    def __init__(self, room_type, short_desc, desc, event=None, interactables=None):
        self.room_type = room_type
        self.short_desc = short_desc
        self.desc = desc
        self.event = event
        self.interactables = interactables
        self.connections = {}

        if self.event: #if there is an event
            self.event_complete = False
        else:
            self.event_complete = True

        self.visited = False

    def __repr__(self):
        str = f'{self.desc}\n'
        if self.interactables:
            for interactable in self.interactables:
                str += f"{Helper.string_color(interactable.desc, 'o')}\n"
        if self.connections:
            for connection in self.connections:
                str += f"To the {Helper.string_color(f'{connection.capitalize()}: {self.connections[connection].short_desc.lower()}', 'g')}\n"
        return str

    def connection_exists(self, direction):
        if direction in self.connections:
            return True
        else:
            return False
        
    def connect(self, direction, room):
        #Connect the room in the direction
        self.connections[direction] = room

        #Get opposite direction
        opposites = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east"
        }
        opposite_direction = opposites.get(direction)

        #Connect self to room if not already connected
        if not room.connection_exists(opposite_direction):
            room.connect(opposite_direction, self)
    
    def visit(self, player):
        print(self)
        if not self.event_complete:
            result = self.event.func(player)
            if result:
                self.event_complete = True
            else:
                return False
        self.visited = True
        Helper.clear_screen()
        print(self)
        return True
    
    def interact(self, player, str):
        if self.interactables:
            scores = [match_count(interactable.name, str) for interactable in self.interactables]
            max_score = max(scores)

            best_matches = [i for i, score in enumerate(scores) if score == max_score]

            if len(best_matches) == 1:
                if self.interactables[best_matches[0]].func(player):
                    self.interactables.remove(self.interactables[best_matches[0]])
            else:
                # Step 4: If too many matches
                print("Invalid Answer: try typing \'help\' for a list of commands.")


class Dungeon:
    def __init__(self, events, location, max_secret_rooms=0):
        #Get Descriptions and Interactables based on location
        if location == "barrens":
            descriptions = barrens_descriptions
            interactables = Interactable.get_interactables_by_location(location)


        self.max_secret_rooms = max_secret_rooms
        self.start = None

        shuffle(events)
        shuffle(descriptions)

        self.rooms = []

        self.generate_dungeon(events, descriptions, interactables)
    
    def generate_dungeon(self, events, descriptions, interactables):
        #Get Boss Event if Possible
        boss_events = []
        boss_event = None
        for event in events:
            if event.flag:
                if 'boss' in event.flag:
                    boss_events.append(event)
        if boss_events:
            boss_event = choice(boss_events)
            events.remove(boss_event)

        #Create Starting Room
        i = 0
        starting_room = Room("start", descriptions[0][0], descriptions[0][1])
        self.rooms.append(starting_room)
        self.start = starting_room
        i += 1

        #Calculate how many Regular Rooms Are Needed to meet Events
        if boss_event:
            regular_rooms_needed = len(events)
        else:
            regular_rooms_needed = len(events) + 1

        #Create and connect Regular Rooms
        while i < regular_rooms_needed:
            #Generate Interactables based on chances for regular rooms
            objects = []
            for interactable in interactables:
                if randint(1, 100) <= interactable.chance:
                    objects.append(interactable)
            if objects:
                new_room = Room("regular", descriptions[i][0], descriptions[i][1], events[i - 1], objects)
            else:
                new_room = Room("regular", descriptions[i][0], descriptions[i][1], events[i - 1])
            random_room = choice(self.rooms)
            directions = ["north", "south", "east", "west"]
            while directions:
                random_direction = choice(directions)
                directions.remove(random_direction)
                if not random_room.connection_exists(random_direction):
                    random_room.connect(random_direction, new_room)
                    self.rooms.append(new_room)
                    i += 1
                    break
        
        #Create and connect Boss Room if Boss Event exists
        if boss_event:
            boss_room = Room("boss", descriptions[i][0], descriptions[i][1], boss_event)
            while i != len(events) + 1:
                random_room = choice(self.rooms)
                if random_room != self.start:
                    directions = ["north", "south", "east", "west"]
                    while directions:
                        random_direction = choice(directions)
                        directions.remove(random_direction)
                        if not random_room.connection_exists(random_direction):
                            random_room.connect(random_direction, boss_room)
                            self.rooms.append(boss_room)
                            i += 1
                            break
