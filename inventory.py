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

        answer = Helper.prompt(["Venture Onward", "Rest", "Inventory", "Status", "Save Game"])
    
        if answer == 0:
            return
        elif answer == 1:
            rest(player)
        elif answer == 2:
            inventory(player)
        elif answer == 3:
            player.view_stats()
        elif answer == 4:
            input("Save functionality is coming soon!")

def rest(player):
    player.chp = player.hp
    player.ctp = player.tp
    player.cmp = player.mp
    
    print(f"{player.name} slept and felt well rested.")
    input("Recovered HP, TP and MP.")

def inventory(player):
    while True:
        Helper.clear_screen()
        Helper.make_banner('INVENTORY')

        answer = Helper.prompt(["Weapons", "Armors", "Skills", "Spells", "Items", "Status", "Conditions", "Go Back"])

        if answer == 0:
            view_weapons(player)
        elif answer == 1:
            view_armors(player)
        elif answer == 2:
            view_skills(player)
        elif answer == 3:
            view_spells(player)
        elif answer == 4:
            view_items(player)
        elif answer == 5:
            player.view_stats()
        elif answer == 6:
            view_conditions(player)
        elif answer == 7:
            return

def view_weapons(player):
    while True:  # Loop to return to the weapon menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Weapons")

        weapon_choices = []
        
        # Create a list of weapon choices for inquirer
        for item in player.inv:
            if isinstance(Weapon.get_weapon(item['name']), Weapon):
                weapon = Weapon.get_weapon(item['name'])
                weapon_info = f"{weapon.name}"
                if weapon.name == player.EQweapon.name:
                    weapon_info += " (Equipped)"
                weapon_choices.append(weapon_info)

        # Add an option to go back
        weapon_choices.append("Go Back")

        answer = Helper.prompt(weapon_choices)

        if answer == (len(weapon_choices) - 1): #Go Back
            return

        weapon_name = weapon_choices[answer].split(" (")[0]
        weapon = Weapon.get_weapon(weapon_name)  # Get the weapon instance

        # Display weapon details
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

        # Ask if the player wants to equip or unequip the weapon
        if player.EQweapon.name == weapon.name:  # Currently equipped
            while True:
                print("Do you want to unequip this weapon? (y/n)")
                ans = Helper.yes_or_no()
                
                if ans == 1:  # Yes
                    player.unequip_weapon(weapon)
                    break
                elif ans == 0:  # No
                    break

        else:  # Not equipped
            while True:
                print("Do you want to equip this weapon? (y/n)")
                ans = Helper.yes_or_no()
                
                if ans == 1:  # Yes
                    player.equip_weapon(weapon)
                    break
                elif ans == 0:  # No
                    break

def view_armors(player):
    while True:  # Loop to return to the armor menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Armor")

        armor_choices = []

        for item in player.inv:
             if isinstance(Armor.get_armor(item['name']), Armor):
                armor = Armor.get_armor(item['name'])
                armor_info = f"{armor.name}"
                if item['name'] == player.EQarmor.name:
                    armor_info += " (Equipped)"
                armor_choices.append(armor_info)

        # Add an option to go back
        armor_choices.append("Go Back")

        answer = Helper.prompt(armor_choices)

        if answer == (len(armor_choices) - 1):
            break

        armor_name = armor_choices[answer].split(" (")[0]
        armor = Armor.get_armor(armor_name)  # Get the armor instance

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

        # Ask if the player wants to equip or unequip the armor
        if player.EQarmor.name == armor.name:  # Currently equipped
            while True:
                print("Do you want to unequip this armor? (y/n)")
                ans = Helper.yes_or_no()
                
                if ans == 1:  # Yes
                    player.unequip_armor(armor)
                    break
                elif ans == 0:  # No
                    break

        else:  # Not equipped
            while True:
                print("Do you want to equip this weapon? (y/n)")
                ans = Helper.yes_or_no()
                
                if ans == 1:  # Yes
                    player.equip_armor(armor)
                    break
                elif ans == 0:  # No
                    break

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

def view_items(player):
    while True:  # Loop to return to the items menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Items")

        item_choices = []
        
        # Create a list of item choices for inquirer, only including Item objects
        for inv_item in player.inv:
            if isinstance(Item.get_item(inv_item["name"]), Item):
                name = inv_item["name"]
                count = inv_item["count"]
                item_choices.append(f"{name} - {count}")

        # Add an option to go back
        item_choices.append("Go Back")

        answer = Helper.prompt(item_choices)

        if answer == (len(item_choices) - 1):
            break

        item_name = item_choices[answer].split(" - ")[0]
        item = Item.get_item(item_name)  # Get the item instance
        item_in_inventory = next((i for i in player.inv if i['name'] == item.name))

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
                    item.func(player)
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
