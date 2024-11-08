#Import
import inquirer
from random import randint

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

    def __init__(self, name, locations, desc, max, func, flag=None):
        self.name = name
        self.locations = locations
        self.desc = desc
        self.max = max
        self.func = func
        self.flag = flag
        Event.all_events.append(self)
    
    @classmethod
    def get_events_by_location(cls, location):
        events = []
        for event in cls.all_events:
            if location in event.locations:
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
        con=1 + randint(0, 1),
        mag=-1,
        str=1 + randint(0, 1),
        int=-1,
        dex=3,
        lck=3 + randint(0, 2),
        df=0,
        mdf=0,
        weapon=Weapon.get_weapon('Club'),
        armor=Armor.get_armor('Cloth'),
        skills=[Skill.get_skill('Heavy Blow')],
        spells=[],
        inv=[Weapon.get_weapon('Club'), Armor.get_armor('Cloth')]
    )
    input("You are suddenly attacked by a Goblin!")
    combat(player, enemy)

def kobold_battle(player):
    enemy = Enemy(
        name='Kobold',
        con=1 + randint(1, 2),
        mag=-1,
        str=0 + randint(0, 1),
        int=-1,
        dex=3 + randint(0, 2),
        lck=1 + randint(0, 1),
        df=5,
        mdf=0,
        weapon=Weapon.get_weapon('Sling'),
        armor=Armor.get_armor('None'),
        skills=[Skill.get_skill('Quick Strike')],
        spells=[],
        inv=[Weapon.get_weapon('Sling')]
    )
    input("You are suddenly attacked by a Kobold!")
    combat(player, enemy)

def boulder(player):
    print(f"While walking along the gravel path by boundless hills,")
    print(f"suddenly a boulder begins rolling toward you down the slope!")
    questions = [
        inquirer.List('choice',
            message="Act fast or get hit",
            choices=["Stop It (Strength)", "Dodge (Dexterity)", "Pray (Luck)", "Take the Hit (Lose HP)"],
        ),
    ]
    answer = inquirer.prompt(questions)
    action = answer['choice']
    if action == "Stop It (Strength)":
        check = player.get_str() + randint(0, player.get_lck())
        print(f"Strength Check: {check}")
        input(f"Needed: 20")
        if check < 20:
            player.chp -= 10
            input(f"{player.name} gets hit by the boulder and takes 10 damage.")
        else:
            input(f"In a rush of adrenaline you successfully manage to redirect the boulder.")
    elif action == "Dodge (Dexterity)":
        check = player.get_dex() + randint(0, player.get_lck())
        print(f"Dexterity Check: {check}")
        input(f"Needed: 5")
        if check < 5:
            player.chp -= 10
            input(f"{player.name} gets hit by the boulder and takes 10 damage.")
        else:
            input(f"You deftly sidestep the boulder, avoiding it completely.")
    elif action == "Pray (Luck)":
        check = randint(0, player.get_lck())
        print(f"Luck Check: {check}")
        input(f"Needed: 10")
        if check < 10:
            player.chp -= 10
            input(f"{player.name} gets hit by the boulder and takes 10 damage.")
        else:
            print("When the boulder is about to strike you, it suddenly splits into two.")
            gold = 0 #Get random gold
            input(f"Inside the boulder, you find {gold}. Isn't that something.")
    else:   #take the hit
        player.chp -= 10
        input(f"{player.name} gets hit by the boulder and takes 10 damage.")
    if player.chp <= 0:
        input(f"{player.name} died.")
        Helper.clear_screen()
        Helper.make_banner("GAME OVER", True)
        print(f"{player.name} was flattened by a boulder.")
        input(">> ")
        exit()


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
    )
]