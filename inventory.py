#Imports
from helper import Helper
from data.weapons import Weapon
from data.armors import Armor
from data.skills import Skill
from data.spells import Spell
from data.items import Item

def camp(player):
    while True:
        Helper.clear_screen()
        Helper.make_banner(player.location.upper())
        Helper.make_banner('CAMP')
        print(f"{player.name} the level {player.lvl} {player.race.name} {player.job.name}")
        print(f"HP: {Helper.render_hp_bar(player.chp, player.hp)}")
        if player.tp != 0:
            print(f"TP: {Helper.render_bar(player.ctp, player.tp, 'dg')}")
        if player.mp != 0:
            print(f"MP: {Helper.render_bar(player.cmp, player.mp, 'b')}")
        print(f"XP: {player.xp}/{player.lvlnxt} - Gold: {player.gold}")

        answer = Helper.handle_commands("camp")

        if answer.name == "Use":
            for inv_item in player.inv:
                if answer.vals in inv_item["name"].lower():
                    item_name = inv_item["name"]                    
                item = Item.get_item(item_name)
            if item:
                if item.can_use(player):
                    item.func(player)
            else:
                input(f"{player.name} cannot use the {answer.vals} because it isn't a consumable.")
        elif answer.name == "View":
            for inv_item in player.inv:
                if answer.vals in inv_item["name"].lower():
                    item_name = inv_item["name"]
            if isinstance(Weapon.get_weapon(item_name), Weapon):
                weapon = Weapon.get_weapon(item_name)
                Helper.make_banner(f"{weapon.name}")
                print(f"Description: {weapon.desc}")
                for item in player.inv:
                    if isinstance(Weapon.get_weapon(item['name']), Weapon):
                        print(f"Count: {item['count']}")
                print(f"Attack: {weapon.atkmin} to {weapon.atkmax}")
                print(f"Magic Attack: {weapon.matkmin} to {weapon.matkmax}")
                if weapon.req1a:
                    print(f"Requirements: {weapon.req1a.upper()}: {weapon.req1m}")
                    if weapon.req2a:
                        print(f"              {weapon.req2a.upper()}: {weapon.req2m}")
                input()
            elif isinstance(Armor.get_armor(item_name), Armor):
                armor = Armor.get_armor(item_name)
                # Display armor details
                Helper.make_banner(f"{armor.name}")
                print(f"Description: {armor.desc}")
                for item in player.inv:
                    if isinstance(Armor.get_armor(item['name']), Armor):
                        print(f"Count: {item['count']}")
                print(f"Defense: {armor.df}")
                print(f"Magic Defense: {armor.mdf}")
                if armor.reqa:
                    print(f"Requires: {armor.reqa.upper()}: {armor.reqm}")
                input()
            elif isinstance(Item.get_item(item_name), Item):
                item = Item.get_item(item_name)
                # Display item details
                Helper.make_banner(f"{item.name}")
                print(f"Description: {item.desc}")
                input()
            else: #not a valid item
                input(f"{player.name} cannot look at the {item_name} because it doesn't exist.") 
        elif answer.name == "Rest":
            rest(player)
        elif answer.name == "Inventory":
            inventory(player)
        elif answer.name == "Skills":
            view_skills(player)
        elif answer.name == "Spells":
            view_spells(player)
        elif answer.name == "Status":
            player.view_stats()
        elif answer.name == "Conditions":
            view_conditions(player)
        elif answer.name == "Save":
            Helper.save(player)
        elif answer.name == "Leave":
            return

def rest(player):
    player.chp = player.hp
    player.ctp = player.tp
    player.cmp = player.mp
    
    print(f"{player.name} slept and felt well rested.")
    input("Recovered HP, TP and MP.")

def inventory(player):
    while True:
        Helper.clear_screen()
        Helper.make_banner('INVENTORY', True)

        #Sort our inv items into catagories: Weapons, Armors, Consumables
        weapons = []
        armors = []
        consumables = []
        for item in player.inv:
            if isinstance(Weapon.get_weapon(item["name"]), Weapon):
                str = f"{item['name']} {item['count']}"
                if Weapon.get_weapon(item["name"]) == player.EQweapon:
                    str += " (Equipped)"
                weapons.append(str)
            elif isinstance(Armor.get_armor(item["name"]), Armor):
                str = f"{item['name']} {item['count']}"
                if Armor.get_armor(item["name"]) == player.EQarmor:
                    str += " (Equipped)"
                armors.append(str)
            else: #consumable
                consumables.append(f"{item['name']} {item['count']}")

        #Print our options and add them to commands
        Helper.make_banner('Weapons')
        for weapon in weapons:
            print(weapon)
            print()
        Helper.make_banner('Armors')
        for armor in armors:
            print(armor)
            print()
        Helper.make_banner('Consumables')
        for consumable in consumables:
            print(consumable)
            print()
        
        answer = Helper.handle_commands("inventory")

        if answer.name == "Don":
            player.equip(answer.vals)
        elif answer.name == "Doff": 
            player.unequip(answer.vals)
        elif answer.name == "Use":
            for inv_item in player.inv:
                if answer.vals in inv_item["name"].lower():
                    item_name = inv_item["name"]                    
                item = Item.get_item(item_name)
            if item:
                if item.can_use(player):
                    item.func(player)
            else:
                input(f"{player.name} cannot use the {answer.vals} because it isn't a consumable.")
        elif answer.name == "View":
            for inv_item in player.inv:
                if answer.vals in inv_item["name"].lower():
                    item_name = inv_item["name"]
            if isinstance(Weapon.get_weapon(item_name), Weapon):
                weapon = Weapon.get_weapon(item_name)
                Helper.make_banner(f"{weapon.name}")
                print(f"Description: {weapon.desc}")
                for item in player.inv:
                    if isinstance(Weapon.get_weapon(item['name']), Weapon):
                        print(f"Count: {item['count']}")
                print(f"Attack: {weapon.atkmin} to {weapon.atkmax}")
                print(f"Magic Attack: {weapon.matkmin} to {weapon.matkmax}")
                if weapon.req1a:
                    print(f"Requirements: {weapon.req1a.upper()}: {weapon.req1m}")
                    if weapon.req2a:
                        print(f"              {weapon.req2a.upper()}: {weapon.req2m}")
                input()
            elif isinstance(Armor.get_armor(item_name), Armor):
                armor = Armor.get_armor(item_name)
                # Display armor details
                Helper.make_banner(f"{armor.name}")
                print(f"Description: {armor.desc}")
                for item in player.inv:
                    if isinstance(Armor.get_armor(item['name']), Armor):
                        print(f"Count: {item['count']}")
                print(f"Defense: {armor.df}")
                print(f"Magic Defense: {armor.mdf}")
                if armor.reqa:
                    print(f"Requires: {armor.reqa.upper()}: {armor.reqm}")
                input()
            elif isinstance(Item.get_item(item_name), Item):
                item = Item.get_item(item_name)
                # Display item details
                Helper.make_banner(f"{item.name}")
                print(f"Description: {item.desc}")
                input()
            else: #not a valid item
                input(f"{player.name} cannot look at the {item_name} because it doesn't exist.")  
        else: #back
            return

def view_skills(player):
    while True:
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Skills")

        skill_choices = []

        for skill in player.skills:
            skill_info = f"{skill.name}"
            if skill in player.EQskills:
                skill_choices.append(f"{skill_info} (Prepared)")
            else:
                skill_choices.append(skill_info)

        skill_choices.append("Go Back")

        answer = Helper.prompt(skill_choices)

        if answer == (len(skill_choices) - 1):
            break

        skill_name = skill_choices[answer].split(" (")[0]
        skill = Skill.get_skill(skill_name)  # Get the skill instance

        Helper.make_banner(f"{skill.name}")
        print(f"Description: {skill.desc}")
        print(f"TP Cost: {skill.cost}")
        print(f"Requirements: {skill.reqa.upper()}: {skill.reqm}")

        if skill not in player.EQskills:
            while True:
                print(f"Do you want to prepare {skill.name}? (y/n)")
                ans = Helper.yes_or_no()
                if ans == 1:
                    player.equip_skill(skill)
                    break
                elif ans == 0:
                    break
        else:
            while True:
                print(f"{skill.name} is currently prepared. Do you want to unprepare it? (y/n)")
                ans = Helper.yes_or_no()
                if ans == 1:
                    player.unequip_skill(skill)
                    break
                elif ans == 0:
                    break

def view_spells(player):
    while True:  # Loop to return to the spell menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Spells")

        # Create a list of spells to display
        spell_choices = []

        # List all spells
        for spell in player.spells:
            spell_info = f"{spell.name}"
            if spell in player.EQspells:
                spell_choices.append(f"{spell_info} (Prepaired)")
            else:
                spell_choices.append(spell_info)

        # Add an option to go back
        spell_choices.append("Go Back")

        answer = Helper.prompt(spell_choices)

        if answer == (len(spell_choices) - 1):
            break

        spell_name = spell_choices[answer].split(" (")[0]
        spell = Spell.get_spell(spell_name)  # Get the spell instance

        # Display all attributes of the selected spell
        Helper.make_banner(f"{spell.name}")
        print(f"Description: {spell.desc}")
        print(f"MP Cost: {spell.cost}")
        print(f"Required INT: {spell.reqm}")
        print(f"Type: {spell.type.upper()}")

        # If the spell is not already equipped, check if it can be equipped
        if spell not in player.EQspells:
            while True:
                # Ask if the player wants to equip the spell
                print(f"Do you want to prepare {spell.name}? (y/n)")
                ans = Helper.yes_or_no()
                if ans == 1:  # Yes
                    player.equip_spell(spell)
                    break
                elif ans == 0:  # No
                    break
        else:
            while True:
                # Option to unequip the spell
                print(f"{spell.name} is currently prepared. Do you want to unprepare it? (y/n)")
                ans = Helper.yes_or_no()
                if ans == 1:  # Yes
                    player.unequip_spell(spell)
                    break
                elif ans == 0:  # No
                    break

def view_conditions(player):
    while True:
        Helper.clear_screen()
        Helper.make_banner("CONDITIONS")
        condition_choices = []
        for condition in player.conditions:
            if condition:
                condition_info = f"{condition.name} - {condition.duration} {condition.duration_type}"
                condition_choices.append(condition_info)

        condition_choices.append("Go Back")

        answer = Helper.prompt(condition_choices)

        if answer == (len(condition_choices) - 1):
            break

        condition_name = condition_choices[answer].split(" - ")[0]  # Get the condition name
        for condition in player.conditions:
            if condition and condition.name == condition_name:
                selected = condition
        
        #Display Condition Details
        Helper.make_banner(f"{selected.name}")
        print(f"Type: {selected.type}")
        print(f"Description: {selected.desc}")
        print(f"Duration: {selected.duration_type} {selected.duration}")
        input()
