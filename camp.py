#Imports
import inquirer

#Imports from file
from helper import Helper
from data.weapons import Weapon
from data.armors import Armor
from data.skills import Skill
from data.spells import Spell
from data.items import items

def camp(player):
    while True:
        # Display player information
        Helper.clear_screen()
        Helper.make_banner(player.location.upper())
        Helper.make_banner('CAMP')
        print(f"{player.name} the level {player.lvl} {player.race.name} {player.job.name}")
        print(f"HP: {player.chp}/{player.hp} - TP: {player.ctp}/{player.tp} - MP: {player.cmp}/{player.mp}")

        questions = [
            inquirer.List('choice',
                        message="Choose an option",
                        choices=["Venture Onward", "Rest", "Inventory", "Save Game"],
                        ),
        ]

        answer = inquirer.prompt(questions)
        if handle_camp_choice(answer['choice'], player) == -1:
            return
        
def handle_camp_choice(choice, player):
    if choice == "Venture Onward":
        return -1
    elif choice == "Rest":
        rest(player)
    elif choice == "Inventory":
        inventory(player)
    elif choice == "Save Game":
        print("Save functionality is coming soon!")
        input("(Press enter to continue...) ")
    return

def rest(player):
    player.chp = player.hp
    player.cmp = player.mp
    player.ctp = player.tp
    
    print(f"{player.name} slept and felt well rested.")
    input("(Press enter to continue...) ")

def inventory(player):
    while True:
        Helper.clear_screen()
        # Display Inventory Menu
        Helper.make_banner('INVENTORY')
        
        questions = [
            inquirer.List('choice',
                          message="Please select an option",
                          choices=["Weapons", "Armors", "Skills", "Spells", "Items", "Stats", "Effects", "Go Back"],
                          ),
        ]

        answer = inquirer.prompt(questions)
        choice = answer['choice']  # Get the selected choice

        if handle_inventory_choice(choice, player) == -1:
            return

def handle_inventory_choice(choice, player):
    if choice == "Weapons":
        view_weapons(player)
    elif choice == "Armors":
        view_armors(player)
    elif choice == "Skills":
        view_skills(player)
    elif choice == "Spells":
        view_spells(player)
    elif choice == "Items":
        view_items(player)
    elif choice == "Stats":
        view_stats(player)
    elif choice == "Effects":
        view_effects(player)
    elif choice == "Go Back":
        return -1

def view_weapons(player):
    while True:  # Loop to return to the weapon menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Weapons")
        
        equipped_weapon = player.get_weapon()  # Get the currently equipped weapon
        equipped_name = equipped_weapon.name if equipped_weapon else 'None'

        weapon_choices = []
        
        # Create a list of weapon choices for inquirer
        for item in player.inv:
            weapon = Weapon.get_weapon(item['name'])  # Get the weapon instance
            if weapon:
                weapon_info = f"{weapon.name} - Quantity: {item['count']}"
                if item['name'] == equipped_name:
                    weapon_info += " (Equipped)"
                weapon_choices.append(weapon_info)

        # Add an option to go back
        weapon_choices.append("Go Back")

        # Create the inquirer prompt for weapon selection
        questions = [
            inquirer.List('weapon_choice',
                          message="Select a weapon to view details, equip, or unequip",
                          choices=weapon_choices),
        ]

        answer = inquirer.prompt(questions)

        if answer['weapon_choice'] == "Go Back":
            break  # Exit the loop to go back

        weapon_name = answer['weapon_choice'].split(" - ")[0]  # Get the weapon name
        weapon = Weapon.get_weapon(weapon_name)  # Get the weapon instance

        # Display weapon details
        Helper.make_banner(f"{weapon.name}")
        print(f"Description: {weapon.desc}")
        print(f"Attack: {weapon.atkmin} to {weapon.atkmax}")
        print(f"Magic Attack: {weapon.matkmin} to {weapon.matkmax}")
        if weapon.req1a:
            print(f"Requirements: {weapon.req1a} {weapon.req1m}")
            if weapon.req2a:
                print(f"              {weapon.req2a} {weapon.req2m}")

        # Ask if the player wants to equip or unequip the weapon
        if equipped_name == weapon.name:  # Currently equipped
            while True:
                print("Do you want to unequip this weapon? (y/n)")
                ans = Helper.yes_or_no(input(">> ").lower())
                
                if ans == 1:  # Yes
                    player.unequip_weapon(weapon.name)
                    break
                elif ans == 0:  # No
                    break
        else:  # Not equipped
            while True:
                print("Do you want to equip this weapon? (y/n)")
                ans = Helper.yes_or_no(input(">> ").lower())
                
                if ans == 1:  # Yes
                    player.equip_weapon(weapon.name)  # Pass the weapon name to the equip_weapon method
                    break
                elif ans == 0:  # No
                    break

def view_armors(player):
    while True:  # Loop to return to the armor menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Armor")

        equipped_armor = player.get_armor()  # Get the currently equipped armor
        equipped_name = equipped_armor.name if equipped_armor else 'None'

        armor_choices = []

        # Create a list of armor choices for inquirer
        for item in player.inv:
            armor = Armor.get_armor(item['name'])  # Get the armor instance
            if armor:
                armor_info = f"{armor.name} - Quantity: {item['count']}"
                if item['name'] == equipped_name:
                    armor_info += " (Equipped)"
                armor_choices.append(armor_info)

        # Add an option to go back
        armor_choices.append("Go Back")

        # Create the inquirer prompt for armor selection
        questions = [
            inquirer.List('armor_choice',
                          message="Select an armor to view details, equip, or unequip",
                          choices=armor_choices),
        ]

        answer = inquirer.prompt(questions)

        if answer['armor_choice'] == "Go Back":
            break  # Exit the loop to go back

        armor_name = answer['armor_choice'].split(" - ")[0]  # Get the armor name
        armor = Armor.get_armor(armor_name)  # Get the armor instance

        # Display armor details
        Helper.make_banner(f"{armor.name}")
        print(f"Description: {armor.desc}")
        print(f"Defense: {armor.df}")
        print(f"Magic Defense: {armor.mdf}")
        print(f"Requires: {armor.reqa} {armor.reqm}")

        # Ask if the player wants to equip or unequip the armor
        if equipped_name == armor.name:  # Currently equipped
            while True:
                print("Do you want to unequip this armor? (y/n)")
                ans = Helper.yes_or_no(input(">> ").lower())
                
                if ans == 1:  # Yes
                    player.unequip_armor(armor.name)
                    break
                elif ans == 0:  # No
                    break
        else:  # Not equipped
            while True:
                print("Do you want to equip this armor? (y/n)")
                ans = Helper.yes_or_no(input(">> ").lower())
                
                if ans == 1:  # Yes
                    player.equip_armor(armor.name)  # Pass the armor name to the equip_armor method
                    break
                elif ans == 0:  # No
                    break

def view_skills(player):
    while True:  # Loop to return to the skill menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Skills")

        # Create a list of skills to display
        skill_choices = []

        # List all skills with only name, description, and equipped status
        for skill in Skill.all_skills:
            skill_info = f"{skill.name} - {skill.desc}"
            if skill in player.EQskills:
                skill_choices.append(f"{skill_info} (Equipped)")
            else:
                skill_choices.append(skill_info)

        # Add an option to go back
        skill_choices.append("Go Back")

        # Create the inquirer prompt for skill selection
        questions = [
            inquirer.List('skill_choice',
                          message="Select a skill to view details, equip, unequip, or use",
                          choices=skill_choices),
        ]

        answer = inquirer.prompt(questions)

        if answer['skill_choice'] == "Go Back":
            break  # Exit the loop to go back

        skill_name = answer['skill_choice'].split(" - ")[0]  # Get the skill name
        skill = Skill.get_skill(skill_name)  # Get the skill instance

        # Display full skill details
        Helper.make_banner(f"{skill.name}")
        print(f"Description: {skill.desc}")
        print(f"TP Cost: {skill.cost}")
        print(f"Requirements: {skill.reqa} {skill.reqm}")
        print(f"Type: {skill.type}")

        # Equip, unequip, or use the skill based on player choice
        if skill not in player.EQskills:
            print(f"Do you want to equip {skill.name}? (y/n)")
            ans = Helper.yes_or_no(input(">> ").lower())
            if ans == 1:
                player.equip_skill(skill.name)  # Equip skill with all checks now within equip_skill method
        else:
            print(f"{skill.name} is currently equipped. Do you want to unequip it? (y/n)")
            ans = Helper.yes_or_no(input(">> ").lower())
            if ans == 1:
                player.unequip_skill(skill.name)  # Unequip the skill

            if skill.type == 'outside':
                print(f"{skill.name} is usable outside of combat. Use it? (y/n)")
                ans = Helper.yes_or_no(input(" >> ").lower())
                if ans == 1:
                    skill.skill_func(player)

        input("(Press enter to continue...) ")

def view_spells(player):
    while True:  # Loop to return to the spell menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Spells")

        # Create a list of spells to display
        spell_choices = []

        # List all spells
        for spell in Spell.all_spells:
            spell_info = f"{spell.name} - {spell.desc}"
            if spell in player.EQspells:
                spell_choices.append(f"{spell_info} (Equipped)")
            else:
                spell_choices.append(spell_info)

        # Add an option to go back
        spell_choices.append("Go Back")

        # Create the inquirer prompt for spell selection
        questions = [
            inquirer.List('spell_choice',
                          message="Select a spell to equip or unequip",
                          choices=spell_choices,
                          ),
        ]

        answer = inquirer.prompt(questions)

        if answer['spell_choice'] == "Go Back":
            break  # Exit the loop to go back

        spell_name = answer['spell_choice'].split(" - ")[0]  # Get the spell name
        spell = Spell.get_spell(spell_name)  # Get the spell instance

        # Display all attributes of the selected spell
        Helper.make_banner(f"{spell.name}")
        print(f"Description: {spell.desc}")
        print(f"MP Cost: {spell.cost}")
        print(f"Required Intelligence: {spell.reqm}")
        print(f"Type: {spell.type}")

        # If the spell is not already equipped, check if it can be equipped
        if spell not in player.EQspells:
            # Ask if the player wants to equip the spell
            print(f"Do you want to equip {spell.name}? (y/n)")
            ans = Helper.yes_or_no(input(">> ").lower())
            if ans == 1:  # Yes
                player.equip_spell(spell.name)
            elif ans == 0:  # No
                print("Spell not equipped.")
        else:
            # Option to unequip the spell
            print(f"{spell.name} is currently equipped. Do you want to unequip it? (y/n)")
            ans = Helper.yes_or_no(input(" >> ").lower())
            if ans == 1:  # Yes
                player.unequip_spell(spell.name)
            elif ans == 0:  # No
                print("Spell not unequipped.")

        input("(Press enter to continue...) ")

def view_items(player):
    while True:  # Loop to return to the items menu
        Helper.clear_screen()
        Helper.make_banner(f"{player.name}'s Items")

        item_choices = []
        
        # Create a list of item choices for inquirer, only including Item objects
        for inv_item in player.inv:
            item = next((i for i in items if i.name == inv_item['name']), None)  # Get the Item instance
            if item:
                item_info = f"{item.name} - Quantity: {inv_item['count']}"
                item_choices.append(item_info)

        # Add an option to go back
        item_choices.append("Go Back")

        # Create the inquirer prompt for item selection
        questions = [
            inquirer.List('item_choice',
                          message="Select an item to use or view details",
                          choices=item_choices,
                          ),
        ]

        answer = inquirer.prompt(questions)

        if answer['item_choice'] == "Go Back":
            break  # Exit the loop to go back

        item_name = answer['item_choice'].split(" - ")[0]  # Get the item name
        item = next((i for i in items if i.name == item_name), None)  # Find the item instance

        if item:
            # Display item details
            Helper.make_banner(f"{item.name}")
            print(f"Description: {item.desc}")

            # Ask if the player wants to use the item
            while True:
                print("Do you want to use this item? (y/n)")
                ans = Helper.yes_or_no(input(">> ").lower())
                
                if ans == 1:  # Yes
                    # Check quantity in inventory
                    item_in_inventory = next((i for i in player.inv if i['name'] == item_name), None)
                    if item_in_inventory and item_in_inventory['count'] > 0:
                        # Call the item's use function
                        if item.func(player):  # Pass the player object
                            item_in_inventory['count'] -= 1  # Decrease quantity
                            # Remove the item from inventory if count goes to 0
                            if item_in_inventory['count'] <= 0:
                                player.inv.remove(item_in_inventory)
                        else:
                            print("Item could not be used.")
                    break
                elif ans == 0:  # No
                    print("Item not used.")
                    break

        input("(Press enter to continue...) ")

def view_stats(player):
    Helper.clear_screen()
    Helper.make_banner(f"{player.name}'s Stats")
    print(f"Race: {player.race.name}")
    print(f"Class: {player.job.name}")
    
    # Display player attributes
    print(f"HP: {player.chp}/{player.hp}")
    print(f"MP: {player.cmp}/{player.mp}")
    print(f"TP: {player.ctp}/{player.tp}")
    print(f"XP: {player.lvlup}/{player.lvlnxt} LVL: {player.lvl}")
    print(f"Strength: {player.str}")
    print(f"Constitution: {player.con}")
    print(f"Magic: {player.mag}")
    print(f"Intelligence: {player.int}")
    print(f"Dexterity: {player.dex}")
    print(f"Luck: {player.lck}")
    print(f"Physical Defense: {player.df}")
    print(f"Magical Defense: {player.mdf}")

    # Display equipped weapon details
    equipped_weapon = player.get_weapon()
    print(f"Equipped Weapon: {equipped_weapon.name if equipped_weapon else 'None'}")

    # Display equipped armor details
    equipped_armor = player.get_armor()
    print(f"Equipped Armor: {equipped_armor.name if equipped_armor else 'None'}")

    # Dislay equipped spell and skill details
    equipped_spells = [spell.name for spell in player.EQspells]
    print(f"Equipped Spells: {', '.join(equipped_spells) if equipped_spells else 'None'}")
    equipped_skills = [skill.name for skill in player.EQskills]
    print(f"Equipped Skills: {', '.join(equipped_skills) if equipped_skills else 'None'}")

    input("(Press enter to continue...) ")

def view_effects(player):
    Helper.clear_screen()
    print("Viewing effects...")
    input("(Press enter to continue...) ")