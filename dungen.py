#Imports
from random import shuffle, choice, randint

from helper import Helper
from data.interactables import Interactable
from data.secrets import Secret_Interactable, Secret

class Room:
    def __init__(self, room_type, short_desc, desc, event=None, interactables=[]):
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
            for direction, connected_room in self.connections.items():
                # Handle secret room connections
                if connected_room.room_type == "secret":
                    is_blocked = False
                    if self.interactables:
                        for interactable in self.interactables:
                            if isinstance(interactable, Secret_Interactable):
                                if interactable.blocks == connected_room.event.name:
                                    is_blocked = True
                                    break
                    if not is_blocked:
                        str += f"{Helper.string_color(f'To the {direction.capitalize()}: {connected_room.short_desc.lower()}', 'p')}\n"
                # Handle non-secret room connections
                else:
                    str += f"{Helper.string_color(f'To the {direction.capitalize()}: {connected_room.short_desc.lower()}', 'g')}\n"
            
            return str

    def connection_exists(self, direction):
        if direction in self.connections:
            connected_room = self.connections[direction]
            if connected_room.room_type == "secret":
                    is_blocked = False
                    if self.interactables:
                        for interactable in self.interactables:
                            if isinstance(interactable, Secret_Interactable):
                                if interactable.blocks == connected_room.event.name:
                                    is_blocked = True
                                    break
                    if not is_blocked:
                        return True
                    else:
                        return False
            else:
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
    
    def interact(self, player, interactable_name):
        if self.interactables:
            for interactable in self.interactables:
                if interactable_name in interactable.name:
                    response = interactable.func(player)
                    if response:
                        self.interactables.remove(interactable)
        else: #no interactables
            print("Invalid Answer: try typing \'help\' for a list of commands.")

class Dungeon:
    def __init__(self, events, descriptions, location):
        self.location = location
        #Get Descriptions and Interactables based on location

        self.start = None
        self.boss = None

        shuffle(events)
        shuffle(descriptions)

        self.rooms = []

        self.generate_dungeon(events, descriptions)
    
    def generate_dungeon(self, events, descriptions):
        #prep stuff
        interactables = Interactable.get_interactables_by_location(self.location)

        #Get Boss Event
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

        #Create and connect Regular Rooms
        while i < len(events):
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
            else:
                break  # Exit if no directions work
        
        #Create and connect Boss Room
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
                        self.boss = boss_room
                        i += 1
                        break
                else:
                    break  # Exit if no directions work
        
        #determine how many secret rooms we should make if any
        if len(events) < len(descriptions) - 2: #have enough descriptions minus starting room and boss room
            secret_room_num = (len(descriptions) - 2) - len(events) #the possible number of secret rooms based on description amount
            while secret_room_num >= 1:  # while we have secret rooms
                if randint(1, 100) <= 11:  # chance for secret rooms
                    secret_event = choice(Secret.get_secrets_by_location(self.location))
                    secret_room = Room("secret", descriptions[i][0], descriptions[i][1], secret_event)
                    room_added = False
                    while not room_added:
                        random_room = choice(self.rooms)
                        if random_room != self.start and random_room != self.boss:
                            directions = ["north", "south", "east", "west"]
                            while directions:
                                random_direction = choice(directions)
                                directions.remove(random_direction)
                                if not random_room.connection_exists(random_direction):
                                    secret_interactable = choice(Secret_Interactable.get_secret_interactables_by_location(self.location))
                                    secret_interactable.blocks = secret_event.name

                                    # Avoid side effects by creating a new list
                                    random_room.interactables = [
                                        i for i in random_room.interactables
                                        if i.name != secret_interactable.name
                                    ]
                                    random_room.interactables.append(secret_interactable)

                                    random_room.connect(random_direction, secret_room)
                                    self.rooms.append(secret_room)
                                    room_added = True
                                    i += 1
                                    break
                            else:
                                break  # Exit if no directions work
                secret_room_num -= 1


