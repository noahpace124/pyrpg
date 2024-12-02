#Imports
from random import randint

from helper import Helper
from combat import combat
from ..enemy import Enemy
from ..weapons import Weapon
from ..armors import Armor
from ..skills import Skill
from ..spells import Spell

#Event Functions
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
    return combat(player, enemy)
    
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
    return combat(player, enemy)

def boulder(player):
    print(f"While walking along the gravel path by boundless hills,")
    print(f"suddenly a boulder begins rolling toward you down the slope!")
    print("Act fast of get hit: ")
    choices = ["Stop It (Strength)", "Dodge (Dexterity)", "Pray (Luck)", "Take the Hit (Lose HP)"]
    answer = Helper.prompt(choices)
    action = choices[answer]
    if action == "Stop It (Strength)":
        check = player.get_str() + randint(0, player.get_lck())
        print(f"Strength Check: {check}")
        input(f"Needed: 20")
        if check < 20:
            player.chp -= 10
            input(f"{player.name} gets hit by the boulder and takes {Helper.string_color('10', 'r')} damage.")
        else:
            input(f"In a rush of adrenaline you successfully manage to redirect the boulder.")
            Helper.award_xp(player, 600)
    elif action == "Dodge (Dexterity)":
        check = player.get_dex() + randint(0, player.get_lck())
        print(f"Dexterity Check: {check}")
        input(f"Needed: 5")
        if check < 5:
            player.chp -= 10
            input(f"{player.name} gets hit by the boulder and takes {Helper.string_color('10', 'r')} damage.")
        else:
            input(f"You deftly sidestep the boulder, avoiding it completely.")
            Helper.award_xp(player, 300)
    elif action == "Pray (Luck)":
        check = randint(0, player.get_lck())
        print(f"Luck Check: {check}")
        input(f"Needed: 10")
        if check < 10:
            player.chp -= 10
            input(f"{player.name} gets hit by the boulder and takes {Helper.string_color('10', 'r')} damage.")
        else:
            print("When the boulder is about to strike you, it suddenly splits into two.")
            gold = 11 * (1 + randint(0, player.get_lck()))
            input(f"Inside the boulder, you find {gold}. Isn't that something.")
    else:   #take the hit
        player.chp -= 10
        input(f"{player.name} gets hit by the boulder and takes {Helper.string_color('10', 'r')} damage.")
    if player.chp <= 0:
        input(f"{player.name} died.")
        Helper.clear_screen()
        Helper.make_banner("GAME OVER", True)
        print(f"{player.name} was flattened by a boulder.")
        input(">> ")
        exit()
    return True

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
    if 'goblin shaman boss' not in player.flags:
        print("Coming close to the end of the barrens you see some lightning crackling in the distance.")
        print("Upon coming closer you see what apears to be another standard goblin, however this one wields a staff.")
        print("Do you want to approach or retreat for now? ")
        choices = ["Approach (Fight Boss)", "Retreat (Previous Room)"]
        answer = Helper.prompt(choices)
        action = choices[answer]
        if action == 'Approach (Fight Boss)':
            result = combat(player, enemy)
            if result: #won
                player.flags.append('goblin shaman boss')
                if 'barrens complete' not in player.flags:
                    player.flags.append('barrens complete')
                    return True
            else: #ran
                return False
        else: #Retreat
            input("You retreat to the previous area before you are spotted by the goblin.")
            return False
    else: #barrens boss has been defeated
        print("You spot another staff wielding goblin in the distance.")
        print("Do you want to approach or retreat? ")
        choices = ["Approach (Fight Boss)", "Retreat (Previous Room)"]
        answer = Helper.prompt(choices)
        action = choices[answer]
        if action == 'Approach (Fight Boss)':
            return combat(player, enemy)
        else: #
            input("You retreat to the previous area before you are spotted by the goblin.")
            return False

#Interactables
def abandoned_sack(player):
    print("You approach the abandoned sack. It appears to be moist and might not be safe to touch.")
    print("Do you still want to reach inside?")
    response = Helper.yes_or_no()
    if response == 1:
        if randint(1, 100) >= (50 - randint(0, player.getlck())): #Chance for good vs bad
            gold = 6 * (1 + randint(0, player.get_lck()))
            input(f"You reach inside and while uncomfortable, you manage to pull out {gold} gold! Lucky!")
            return True
        else:
            input(f"You reach inside the sack, but immediately your hand starts to burn. You take {Helper.string_color('5', 'r')} damage from the liquid.")
            player.chp -= 5
            if player.chp <= 0:
                input(f"{player.name} died.")
                Helper.clear_screen()
                Helper.make_banner("GAME OVER", True)
                print(f"{player.name} died from an unknown liquid.")
                input(">> ")
                exit()
            return True
    else:
        input("You decide not to reach in a bad with who knows what inside. Better safe than sorry.")
        return False


# List of rooms in the Barrens
barrens_descriptions = [
    ["A flat, dusty expanse stretches endlessly.", 
     "A featureless plain of cracked earth and loose dust. There's nothing "
     "to break the monotony, just the faint hiss of wind dragging sand along the ground."],
    
    ["A plateau of cracked, uneven rock looms ahead.", 
     "The plateau's surface is uneven and split by deep cracks. The surrounding area "
     "offers no clues about how this land came to be so lifeless."],
    
    ["The remains of a dry riverbed cut through the terrain.", 
     "This riverbed, long devoid of water, carves a winding path through the wasteland. "
     "Its dry, crumbling banks offer no sign of life."],
    
    ["A wide clearing coated in fine gray ash.", 
     "The ground here is blanketed in a thin layer of ash, giving the area a somber, "
     "lifeless feel. The source of the ash is a mystery, but nothing grows here now."],
    
    ["A crumbling outpost lies abandoned.", 
     "What remains of this outpost are shattered walls and scattered debris. The air is "
     "still, as though even the wind avoids this place."],
    
    ["A deep, shadowy pit breaks the flat terrain.", 
     "The pit's jagged edges and dark depths suggest danger. Around its edge, the ground "
     "is cracked and loose, as though threatening to give way."],
    
    ["A shallow, parched hollow lies here.", 
     "The hollow is sunken into the ground, its dry soil scattered with faint impressions "
     "of long-dead plants. A faint breeze stirs dust across its surface."],
    
    ["A trail of deep gouges scars the land.", 
     "The trail is marked by deep gouges as if some massive creature once dragged itself "
     "through here. The trail leads off into the wasteland with no end in sight."],
]
