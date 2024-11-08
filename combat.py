#Imports
import inquirer
from random import randint, shuffle

#Imports from File
from helper import Helper
from data.skills import Skill
from data.spells import Spell
from data.items import Item
from data.conditions import Condition

def combat(player, enemy):
    turn_count = 1
    while True:
        Helper.clear_screen()
        Helper.make_banner('COMBAT', True)
        Helper.make_banner(f'Turn {turn_count}')
        print(f'{player.name}: {player.chp}/{player.hp} HP VS {enemy.name}: {enemy.chp}/{enemy.hp} HP')
        print(f'MP: {player.cmp}/{player.mp} - TP: {player.ctp}/{player.tp}')
        
        choices = ['Attack', 'Guard', 'Skills', 'Spells', 'Inventory', 'Status', 'Enemy Status']
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
            combat_win(player, enemy)
            break
        elif res == 1: #run
            input(f"{player.name} managed to run away...")
            break
        elif res == 0: #player loss
            input(f"{player.name} died.")
            Helper.clear_screen()
            Helper.make_banner("GAME OVER", True)
            print(f"{player.name} was killed by the {enemy.name}.")
            input(">> ")
            exit()
        elif res == 3: #3 - correct response, game continues
            player.upkeep()
            enemy.upkeep()
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
    elif choice == "Enemy Status":
        enemy.view_stats()
        return -1
    elif choice == "Run":
        return combat_round(player, enemy, 'run')
    return

def combat_round(player, enemy, obj=None):
    #player option check
    priority = False
    if obj and (isinstance(obj, Skill) or isinstance(obj, Spell)):
        if obj.type == 'priority':
            priority == True
    #enemy option check
    enemy_obj = enemy.get_action()
    enemy_priority = False
    if enemy_obj and (isinstance(enemy_obj, Skill) or isinstance(enemy_obj, Spell)):
        if enemy_obj.type == 'priority':
            enemy_priority = True
    #both use priority
    if priority and enemy_priority:
        priority = False
        enemy_priority = False
    #Start our round
    if (speed_test(player, enemy) or priority) and not enemy_priority: #player is faster
        #player acts
        if obj == None: #atk
            attack(player, enemy)
        elif obj == 'run':
            if speed_test(player, enemy): #player is faster
                return 1 #runs away
            else:
                print(f"{player.name} could not run away!")
        elif isinstance(obj, Item): #item
            obj.func(player)
        else: #skill or spell
            obj.func(player, enemy)
        #check hp
        if enemy.chp <= 0:
            return 2 #player win
        if player.chp <= 0:
            return 0 #player loss
        #enemy acts
        if enemy_obj == None: #atk
            attack(enemy, player)
        else: #skill or spell
            enemy_obj.func(enemy, player)
        #check hp
        if enemy.chp <= 0:
            return 2 #player win
        if player.chp <= 0:
            return 0 #player loss
        #end of round
        return 3
    else: #enemy is faster
        #enemy acts
        if enemy_obj == None: #atk
            attack(enemy, player)
        else: #skill or spell
            enemy_obj.func(enemy, player)
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
            else:
                print(f"{player.name} could not run away!")
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
    dodge_chance = max(defender.get_dodge() - attacker.get_dex(), 0)
    if randint(1, 100) > dodge_chance:
        atk = attacker.get_atk()
        df = defender.get_df(atk)
        dmg = max(atk - df, 1)
        defender.chp -= dmg
        input(f"{attacker.name} {attacker.EQweapon.msg} at {defender.name} for {dmg} damage.")
    else:
        input(f"{defender.name} avoided {attacker.name}\'s attack!")

def guard(player, enemy):
    input(f"{player.name} guards and catches their breath.")
    player.ctp += round(player.get_dex() * 1.33)
    if player.ctp > player.tp:
        player.ctp = player.tp
    player.conditions.append(Condition.get_condition("Defense Up", 1))
    #enemy acts
    enemy_obj = enemy.get_action()
    if enemy_obj == None: #atk
        attack(enemy, player)
    else: #skill or spell
        enemy_obj.func(enemy, player)
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

def combat_win(player, enemy):
    print(f"{enemy.name} was defeated.")
    xp = round(enemy.lvl * (50 / player.lvl))
    print(f"{player.name} gained {xp} experience.")
    player.xp += xp
    points = 0
    while player.xp > player.lvlnxt:
        player.xp -= player.lvlnxt
        player.lvl += 1
        player.lvlnxt = player.lvl * 100
        points += 1
        print(f"{player.name} leveled up to level {player.lvl}!")
    input("(Press enter to continue...) ")
    while points > 0:
        Helper.clear_screen()
        questions = [
            inquirer.List('choice',
                        message="What stat do you want to increase? (Stat Points Remaining: {points})",
                        choices=['Constitution', 'Magic', 'Strength', 'Intelligence', 'Dexterity', 'Luck'],
                        ),
        ]
        answer = inquirer.prompt(questions)
        stat = answer['choice']
        if stat == 'Constitution':
            player.con += 1
            player.hp = 20 + ((player.con - 1) * 5)
        if stat == 'Magic':
            player.mag += 1
        if stat == 'Strength':
            player.str += 1
        if stat == 'Intelligence':
            player.int += 1
            player.mp = 10 + ((player.int - 1) * 5)
        if stat == 'Dexterity':
            player.dex += 1
            player.tp = 10 + ((player.dex - 1) * 5)
        if stat == 'Luck':
            player.lck += 1
        player.chp = player.hp
        player.cmp = player.mp
        player.ctp = player.tp
        points -= 1
    Helper.clear_screen()
    gold = enemy.lvl * (1 + randint(0, player.get_lck()))
    input(f"{player.name} gained {gold} gold.")
    if len(enemy.inv) > 0:
        if randint(1, 100) <= player.get_lck():
            shuffle(enemy.inv)
            item = enemy.inv[0]
            print(f"{player.name} found a {item.name}.")
            player.inv.append({'name': item.name, 'count': 1})
    for condition in player.conditions: #drop all turn based conditions at battle end
        if condition and condition.duration_type == 'turn':
            player.conditions.remove(condition)
    input("(Press enter to continue...) ")