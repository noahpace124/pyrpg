#Imports
from random import randint, shuffle

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
        print(f'{player.name}')
        print(f"HP: {Helper.render_hp_bar(player.chp, player.hp)}")
        if player.tp != 0:
            print(f"TP: {Helper.render_bar(player.ctp, player.tp, 'dg')}")
        if player.mp != 0:
            print(f"MP: {Helper.render_bar(player.cmp, player.mp, 'b')}")
        print(f"{enemy.name}")
        print(f"HP: {Helper.render_bar(enemy.chp, enemy.hp, 'r')}")
        choices = ['Attack', 'Guard']
        for skill in player.EQskills: # Add equipped skills
            skill_info = f"{skill.name}: {skill.cost} TP"
            choices.append(skill_info)
        for spell in player.EQspells: # Add equipped spells
            spell_info = f"{spell.name}: {spell.cost} MP"
            choices.append(spell_info)
        choices.append('Items')
        choices.append('Status')
        choices.append('Enemy Status')
        if 'Boss' not in enemy.flags:
            choices.append('Run')

        answer = Helper.prompt(choices)
        print()

        response = -1
        if choices[answer] == 'Attack':
            response = combat_round(player, enemy)
        elif choices[answer] == 'Guard':
            response = guard(player, enemy)
        elif choices[answer] == 'Items':
            response = combat_inventory(player, enemy)
        elif choices[answer] == 'Status':
            player.view_stats()
        elif choices[answer] == 'Enemy Status':
            enemy.view_stats()
        elif choices[answer] == 'Run':
            response = combat_round(player, enemy, 'run')
        elif isinstance(Skill.get_skill(choices[answer].split(':')[0]), Skill):
            skill = Skill.get_skill(choices[answer].split(':')[0])
            if player.ctp < skill.cost:
                input(f"You don't have enough TP!")
            else:
                response = combat_round(player, enemy, skill)
        elif isinstance(Spell.get_spell(choices[answer].split(':')[0]), Spell):
            if player.cmp < spell.cost:
                input(f"You don't have enough MP!")
            else:
                response = combat_round(player, enemy, spell)

        if response == 2: #player win
            combat_win(player, enemy)
            return True
        elif response == 1: #run
            input(f"{player.name} managed to run away...")
            return False
        elif response == 0: #player loss
            input(f"{player.name} died.")
            Helper.clear_screen()
            Helper.make_banner("GAME OVER", True)
            print(f"{player.name} was killed by the {enemy.name}.")
            input(">> ")
            exit()
        elif response == 3: #3 - correct response, game continues
            enemy.upkeep()
            #check hp
            if enemy.chp <= 0: #enemy dies
                combat_win(player, enemy)
                return True
            player.upkeep()
            if player.chp <= 0: #player dies
                input(f"{player.name} died.")
                Helper.clear_screen()
                Helper.make_banner("GAME OVER", True)
                print(f"{player.name} was killed by a status condition.")
                input(">> ")
                exit()
            
            #increase turn count
            turn_count += 1

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
            if run(player, enemy): #player is faster
                return 1 #runs away
            else:
                input(f"{player.name} could not run away!")
        elif isinstance(obj, Item): #item
            obj.func(player)
        else: #skill or spell
            obj.func(player, enemy)
        #check hp
        if enemy.chp <= 0:
            return 2 #player win
        if player.chp <= 0:
            return 0 #player loss
        print()
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
        print()
        #player acts
        if obj == None: #atk
            attack(player, enemy)
        elif obj == 'run':
            if run(player, enemy): #player is faster
                return 1 #runs away
            else:
                input(f"{player.name} could not run away!")
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
        input(f"{attacker.name} {attacker.EQweapon.msg} at {defender.name} for {Helper.string_color(dmg, 'r')} damage.")
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

def run(player, enemy):
    if randint(1, 100) <= max((player.get_dex() - enemy.get_dex()) * 10, 1) + player.get_lck():
        return True
    else:
        return False

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
        print("Select an item to use: ")

        answer = Helper.prompt(item_choices)

        if item_choices[answer] == "Go Back":
            break  # Exit the loop to go back

        item_name = item_choices[answer].split(": ")[0]  # Get the item name
        item = Item.get_item(item_name)
        item_in_inventory = next((i for i in player.inv if i['name'] == item.name), None)

        # Display item details
        Helper.make_banner(f"{item.name}")
        print(f"Description: {item.desc}")
        print(f"Amount: {item_in_inventory['count']}")

        # Ask if the player wants to use the item
        while True:
            print("Do you want to use this item? (y/n)")
            ans = Helper.yes_or_no()
            
            if ans == 1:  # Yes
                if item.can_use(player):
                    return combat_round(player, enemy, item)
                else:
                    return -1
            elif ans == 0:  # No
                return -1

def combat_win(player, enemy):
    input(f"{enemy.name} was defeated.")
    xp = round((enemy.hp * 10) * max(1 + ((enemy.lvl - player.lvl)/player.lvl), 1))
    Helper.award_xp(player, xp)
    gold = max(enemy.get_lck() * 10, 1) * (1 + randint(0, player.get_lck()))
    player.gold += gold
    input(f"{player.name} gained {gold} gold.")
    print()
    if len(enemy.inv) > 0:
        if randint(1, 100) <= player.get_lck():
            shuffle(enemy.inv)
            item = enemy.inv[0]
            input(f"{player.name} found a {item.name}!")
            player.inv.append({'name': item.name, 'count': 1})
    for condition in player.conditions: #drop all turn based conditions at battle end
        if condition and condition.duration_type == 'turn':
            player.conditions.remove(condition)
    #reset the enemy conditions
    for condition in enemy.conditions: enemy.conditions.remove(condition)