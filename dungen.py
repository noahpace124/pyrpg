#Imports
from random import shuffle, choice

class Room:
    def __init__(self, room_type, short_desc, desc, event=None, objects=None):
        self.room_type = room_type
        self.short_desc = short_desc
        self.desc = desc
        self.event = event
        self.objects = objects
        self.connections = {}

        self.visited = False
    
    def __repr__(self):
        return (f"{self.room_type.upper()[0]}") 

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
    
    def describe(self):
        if not self.visited: #first time here
            self.visited = True
            return self.desc
        else: #every other time here
            return self.short_desc

    
class Dungeon:
    def __init__(self, num_rooms, descriptions, events=None, objects=None, max_secret_rooms=0):
        self.num_rooms = num_rooms
        self.descriptions = descriptions
        self.events = events
        self.objects = objects
        self.max_secret_rooms = max_secret_rooms
        self.start = None

        shuffle(self.descriptions)

        self.rooms = []

        self.generate_dungeon()
    
    def generate_dungeon(self):
        #Create Starting Room
        i = 0
        starting_room = Room("start", self.descriptions[i][0], self.descriptions[i][1])
        self.rooms.append(starting_room)
        self.start = starting_room
        i += 1

        #Create and connect Regular Rooms
        while i < self.num_rooms - 1:
            new_room = Room("regular", self.descriptions[i][0], self.descriptions[i][1])
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
        
        #Create and connect Boss Room
        boss_room = Room("boss", self.descriptions[i][0], self.descriptions[i][1])
        while i != self.num_rooms:
            random_room = choice(self.rooms)
            if random_room.room_type != "start":
                directions = ["north", "south", "east", "west"]
                while directions:
                    random_direction = choice(directions)
                    directions.remove(random_direction)
                    if not random_room.connection_exists(random_direction):
                        random_room.connect(random_direction, boss_room)
                        self.rooms.append(boss_room)
                        i += 1
                        break
