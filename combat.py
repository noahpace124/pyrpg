#Imports
import inquirer
from random import randint

#Imports from File
from helper import Helper
from data.skills import Skill
from data.spells import Spell
from data.items import Item

def combat(player, enemy):
    turn_count = 1
    while True:
        Helper.clear_screen()
        Helper.make_banner('COMBAT', True)
        Helper.make_banner(f'Turn {turn_count}')
        print(f'{player.name}: {player.chp}/{player.hp} HP VS {enemy.name}: {enemy.chp}/{enemy.hp} HP')
        print(f'MP: {player.cmp}/{player.mp} - TP: {player.ctp}/{player.tp}')
        
        choices = ['Attack', 'Guard', 'Skills', 'Spells', 'Inventory', 'Status']
        if 'Boss' not in enemy.flags:
            choices.append('Run')

        questions = [
            inquirer.List('choice',
                        message="Choose an option",
                        choices=choices,
                        ),
        ]

        answer = inquirer.prompt(questions)
        res = handle_combat_choice(answer['choice'], player, enemy)
        if res == 2: #player win
            print('player win')
            break
        elif res == 1: #run
            print('run')
            break
        elif res == 0: #player loss
            print('player loss')
            break
        elif res == -1: #no action taken
            print('no action taken')
        else: #3 - correct response, game continues
            #regen tp and mp
            player.regen()
            enemy.regen()
            #increase turn count
            turn_count += 1

def handle_combat_choice(choice, player, enemy):
    if choice == "Attack":
        return combat_round(player, enemy)
    elif choice == "Guard":
        return guard(player, enemy)
    elif choice == "Skills":
        return use_skill(player, enemy)
    elif choice == "Spells":
        return use_spell(player, enemy)
    elif choice == "Inventory":
        return combat_inventory(player, enemy)
    elif choice == "Status":
        player.view_stats()
        return -1
    elif choice == "Run":
        return combat_round(player, enemy, 'run')
    return

def combat_round(player, enemy, obj=None):
    # GENERATE ENEMY INTENTIONS HERE FOR SKILL PRIORITY
    priority = False
    if obj and (isinstance(obj, Skill) or isinstance(obj, Spell)):
        if obj.type == 'priority':
            priority == True
    if speed_test(player, enemy) or priority: #player is faster
        #player acts
        if obj == None: #atk
            attack(player, enemy)
        elif obj == 'run':
            if speed_test(player, enemy): #player is faster
                return 1 #runs away
        elif isinstance(obj, Item): #item
            obj.func(player)
        else: #skill or spell
            obj.func(player, enemy)
        #check hp
        if enemy.chp <= 0:
            return 2 #player win
        if player.chp <= 0:
            return 0 #player loss
        #enemy acts RIGHT NOW JUST ATKS
        attack(enemy, player)
        #check hp
        if enemy.chp <= 0:
            return 2 #player win
        if player.chp <= 0:
            return 0 #player loss
        #end of round
        return 3
    else: #enemy is faster
        #enemy acts RIGHT NOW JUST ATKS
        attack(enemy, player)
        #check hp
        if enemy.chp <= 0:
            return 2 #player win
        if player.chp <= 0:
            return 0 #player loss
         #player acts
        if obj == None: #atk
            attack(player, enemy)
        elif obj == 'run':
            if speed_test(player, enemy): #player is faster
                return 1 #runs away
        elif isinstance(obj, Item): #item
            obj.func(player)
        else: #skill or spell
            obj.func(player, enemy)
        #check hp
        if enemy.chp <= 0:
            return 2 #player win
        if player.chp <= 0:
            return 0 #player loss
        #end of round
        return 3

def speed_test(player, enemy):
    if player.get_spd() >= enemy.get_spd(): #player is faster or equal
        return True
    else: #enemy is faster
        return False

def attack(attacker, defender):
    atk = attacker.get_atk()
    if crit(attacker, defender):
        print("Critical Hit!")
        atk = atk * 2
    df = defender.get_df(atk)
    dmg = max(atk - df, 1)
    defender.chp -= dmg
    input(f"{attacker.name} {attacker.EQweapon.msg} at {defender.name} for {dmg} damage.")

def crit(attacker, defender):
    return (get_crit_rate(attacker, defender) >= randint(1, 100))

def get_crit_rate(attacker, defender): #always returns at least 1
    return max(int(round(((attacker.lck * 2) / 100) * ((attacker.lvl/defender.lvl) * 100), 0)), 1)

def guard(player, enemy):
    print(f"{player.name} guards and catches their breath.")
    player.ctp += round(player.dex * 1.5)
    if player.ctp > player.tp:
        player.ctp = player.tp
    #enemy acts RIGHT NOW JUST ATKS
    attack(enemy, player)
    #check hp
    if enemy.chp <= 0:
        return 2 #player win
    if player.chp <= 0:
        return 0 #player loss
    #end of round
    return 3

def use_skill(player, enemy):
    #make a list of all skills and 'go back'
    skill_choices = []
    for skill in player.EQskills:
        skill_info = f"{skill.name}: {skill.cost} TP - {skill.desc}"
        skill_choices.append(skill_info)
    skill_choices.append("Go Back")
    #prompt user for skill or to go back
    questions = [
        inquirer.List('skill_choice',
                        message="Select a skill to use or go back",
                        choices=skill_choices),
    ]
    answer = inquirer.prompt(questions)
    #no action taken
    if answer['skill_choice'] == "Go Back":
        return -1
    else:
        #action taken
        skill_name = answer['skill_choice'].split(": ")[0]  # Get the skill name
        skill = Skill.get_skill(skill_name)
        if player.ctp < skill.cost:
            input(f"You don't have enough TP!")
            return -1
        else:
            return combat_round(player, enemy, skill)

def use_spell(player, enemy):
    #make a list of all spells and 'go back'
    spell_choices = []
    for spell in player.EQspells:
        spell_info = f"{spell.name}: {spell.cost} MP - {spell.desc}"
        spell_choices.append(spell_info)
    spell_choices.append("Go Back")
    #prompt user for spell or to go back
    questions = [
        inquirer.List('spell_choice',
                        message="Select a spell to cast or go back",
                        choices=spell_choices),
    ]
    answer = inquirer.prompt(questions)
    #no action taken
    if answer['spell_choice'] == "Go Back":
        return -1
    else:
        #action taken
        spell_name = answer['spell_choice'].split(": ")[0]  # Get the spell name
        spell = Spell.get_spell(spell_name)
        if player.cmp < spell.cost:
            input(f"You don't have enough MP!")
            return -1
        else:
            return combat_round(player, enemy, spell)

def combat_inventory(player, enemy):
    while True:  # Loop to return to the items menu
        item_choices = []
        
        # Create a list of item choices for inquirer, only including Item objects
        for inv_item in player.inv:
            item = Item.get_item(inv_item["name"])
            if isinstance(item, Item):
                item_info = f"{item.name}: {inv_item['count']} - {item.desc}"
                item_choices.append(item_info)

        # Add an option to go back
        item_choices.append("Go Back")

        # Create the inquirer prompt for item selection
        questions = [
            inquirer.List('item_choice',
                          message="Select an item to use",
                          choices=item_choices,
                          ),
        ]

        answer = inquirer.prompt(questions)

        if answer['item_choice'] == "Go Back":
            break  # Exit the loop to go back

        item_name = answer['item_choice'].split(": ")[0]  # Get the item name
        item = Item.get_item(item_name)
        item_in_inventory = next((i for i in player.inv if i['name'] == item.name), None)

        # Display item details
        Helper.make_banner(f"{item.name}")
        print(f"Description: {item.desc}")
        print(f"Amount: {item_in_inventory['count']}")

        # Ask if the player wants to use the item
        while True:
            print("Do you want to use this item? (y/n)")
            ans = Helper.yes_or_no(input(">> ").lower())
            
            if ans == 1:  # Yes
                if item.can_use(player):
                    return combat_round(player, enemy, item)
                else:
                    return -1
            elif ans == 0:  # No
                return -1