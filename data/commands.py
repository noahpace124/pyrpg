class Commands:
    all_commands = []

    def __init__(self, name, args, format, description, menu):
        self.name = name
        self.args = args
        self.format = format
        self.description = description
        self.menu = menu
        self.input = ""
        self.all_commands.append(self)
        
    def __str__(self):
        return self.format + " --> " + self.description
    
    def get_commands(menu):
        commands = []
        for command in Commands.all_commands:
            if menu in command.menu or "all" in command.menu:
                commands.append(command)
        return commands


commands = [
    Commands("Help", 0, "help", "Shows all commands.", ["all"]),
    Commands("Rest", 0, "rest", "Restores all health and mana.", ["camp"]),
    Commands("Inventory", 0, "inv", "Shows all items in your inventory.", ["camp", "places"]),
    Commands("Skills", 0, "skills", "Shows all skills you have.", ["camp"]),
    Commands("Spells", 0, "spells", "Shows all spells you have.", ["camp"]),
    Commands("Status", 0, "status", "Shows your current status.", ["camp"]),
    Commands("Conditions", 0, "conditions", "Shows all status conditions you have.", ["camp"]),
    Commands("Save", 0, "save", "Saves your game.", ["camp"]),
    Commands("Leave", 0, "leave", "Leaves the camp.", ["camp"]),
    Commands("Don", 1, "don <item>", "Equip an item from your inventory.", ["inventory"]),
    Commands("Doff", 1, "doff <item>", "Unequip an item from your inventory.", ["inventory"]),
    Commands("Use", 1, "use <item>", "Use an item from your inventory.", ["camp", "inventory", "places"]),
    Commands("View", 1, "view <item>", "View an item in your inventory.", ["camp", "inventory", "places"]),
    Commands("Back", 0, "back", "Go back.", ["inventory"]),
    Commands("Look", 0, "look", "Look around the room to get details again.", ["places"]),
    Commands("Go", 1, "go <direction>", "Move in <direction> if possible.", ["places"]),
    Commands("Check Out", 1, "check <object>", "Check out an object in the room.", ["places"]),
]