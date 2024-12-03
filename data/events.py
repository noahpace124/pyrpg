#Import
from data.dungeons.barrens import goblin_battle, kobold_battle, boulder, goblin_shaman, barrens_secret

class Event:
    all_events = []

    def __init__(self, name, locations, desc, max, func, flag=None):
        self.name = name
        self.locations = locations
        self.desc = desc
        self.max = max
        self.func = func
        self.flag = flag
        Event.all_events.append(self)
    
    @classmethod
    def get_events_by_location(cls, location, flags=None): #only adds events in player flags
        events = []
        for event in cls.all_events:
            if location in event.locations:
                if event.flag:
                    if flags:
                        if event.flag in flags:
                            events.append(event)
                else:
                    events.append(event)
        return events
    
    @classmethod
    def get_boss_events_by_location(cls, location):
        events = []
        for event in cls.all_events:
            if location in event.locations:
                if event.flag:
                    if 'boss' in event.flag:
                        events.append(event)
        return events

    
    @classmethod
    def get_event(cls, event_name):
        for event in cls.all_events:
            if event.name == event_name:
                return event

events = [
    Event(
        "Goblin Encounter",
        ["barrens"],
        "A basic fight with a goblin.", 
        4,
        goblin_battle
    ),
    Event(
        "Kobold Encounter",
        ["barrens"],
        "A basic fight with a kobold.",
        4,
        kobold_battle
    ),
    Event(
        "Boulder",
        ["barrens"],
        "A boulder is falling toward you!",
        2,
        boulder
    ),
    Event(
        "Goblin Shaman",
        ["barrens"],
        "A goblin shaman want to fight you.",
        1,
        goblin_shaman,
        flag='goblin shaman boss'
    )
]

