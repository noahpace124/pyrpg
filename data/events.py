#Import

#Import from File
from combat import combat
from helper import Helper
from .enemy import Enemy
from .weapons import Weapon
from .armors import Armor
from .skills import Skill
from .spells import Spell

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
        name='Goblin',
        con=1,
        mag=-1,
        str=1,
        int=-1,
        dex=3,
        lck=3,
        df=0,
        mdf=0,
        weapon=Weapon.get_weapon('Club'),
        armor=Armor.get_armor('Cloth'),
        skills=[Skill.get_skill('Quick Strike')]
    )
    Helper.clear_screen()
    input("You are suddenly approached by a Goblin!")
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