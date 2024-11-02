#Import

#Import from File
from combat import combat
from .enemy import Enemy
from .weapons import Weapon
from .armors import Armor

class Event:
    all_events = []

    def __init__(self, name, location, desc, max, func, flag=None):
        self.name = name
        self.location = location
        self.desc = desc
        self.max = max
        self.func = func
        self.flag = flag
        Event.all_events.append(self)
    
    @classmethod
    def get_events_by_location(cls, location):
        events = []
        for event in cls.all_events:
            if event.location == location:
                events.append(event)
        return events
    
    @classmethod
    def get_event(cls, event_name):
        for event in cls.all_events:
            if event.name == event_name:
                return event

#define event functions
def goblin_battle(player):
    enemy = Enemy(
        'Goblin',
        2,
        -1,
        2,
        -1,
        1,
        2,
        0,
        0,
        Weapon.get_weapon('Club'),
        Armor.get_armor('Cloth')
    )

    print("You encounter a Goblin!")
    input("(Press enter to continue...) ")
    combat(player, enemy)

events = [
    Event(
        "Goblin Encounter",
        "barrens",
        "A basic fight with a goblin.",
        4,
        goblin_battle
    )
]