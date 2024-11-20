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
        print(events)
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
        mag=0,
        str=1 + randint(0, 2),
        int=0,
        dex=2,
        lck=2 + randint(0, 1),
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
        con=1 + randint(0, 1),
        mag=0,
        str=0,
        int=0,
        dex=3 + randint(0, 2),
        lck=3 + randint(0, 2),
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
            Helper.award_xp(player, 600)
    elif action == "Dodge (Dexterity)":
        check = player.get_dex() + randint(0, player.get_lck())
        print(f"Dexterity Check: {check}")
        input(f"Needed: 5")
        if check < 5:
            player.chp -= 10
            input(f"{player.name} gets hit by the boulder and takes 10 damage.")
        else:
            input(f"You deftly sidestep the boulder, avoiding it completely.")
            Helper.award_xp(player, 300)
    elif action == "Pray (Luck)":
        check = randint(0, player.get_lck())
        print(f"Luck Check: {check}")
        input(f"Needed: 10")
        if check < 10:
            player.chp -= 10
            input(f"{player.name} gets hit by the boulder and takes 10 damage.")
        else:
            print("When the boulder is about to strike you, it suddenly splits into two.")
            gold = 100 * randint(1, 3)
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

def goblin_shaman(player):
    enemy = Enemy(
        name='Goblin Shaman',
        con=1 + randint(0, 1),
        mag=2 + randint(0, 1),
        str=1 + randint(0, 1),
        int=2,
        dex=2,
        lck=2 + randint(0, 1),
        df=0,
        mdf=0,
        weapon=Weapon.get_weapon('Wooden Staff'),
        armor=Armor.get_armor('Cloth'),
        skills=[Skill.get_skill('Fast Attacks')],
        spells=[Spell.get_spell('Zap')],
        inv=[Weapon.get_weapon('Wooden Staff'), Armor.get_armor('Cloth')]
    )
    Helper.clear_screen()
    if 'barrens boss' not in player.flags:
        print("Coming close to the end of the barrens you see some lightning crackling in the distance.")
        print("Upon coming closer you see what apears to be another standard goblin, however this one wields a staff.")
        questions = [
            inquirer.List('choice',
                message="Do you want to approach or retreat for now?",
                choices=["Approach (Fight Boss)", "Retreat (Return to Camp)"],
            ),
        ]
        answer = inquirer.prompt(questions)
        action = answer['choice']
        if action == 'Approach (Fight Boss)':
            combat(player, enemy)
            player.flags.append('barrens boss')
            if 'barrens complete' not in player.flags:
                player.flags.append('barrens complete')
        else: #Retreat
            input("You return back to your camp before you are spotted by the goblin.")
            if 'barrens complete' not in player.flags:
                player.flags.append('barrens complete')
    else: #barrens boss has been defeated
        print("You spot another staff wielding goblin in the distance.")
        questions = [
            inquirer.List('choice',
                message="Do you want to approach or try to sneak past?",
                choices=["Approach (Fight Boss)", "Go Around (Continue)"]
            ),
        ]
        answer = inquirer.prompt(questions)
        action = answer['choice']
        if action == 'Approach (Fight Boss)':
            combat(player, enemy)
        else: #Continue past
            input("You decide to take a slightly longer route to avoid the fight.")
                

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
        flag='barrens boss'
    )
]