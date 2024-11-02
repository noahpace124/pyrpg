#Import

class Item:
    all_items = []

    def __init__(self, name, desc, can_use, func):
        self.name = name
        self.desc = desc
        self.can_use = can_use
        self.func = func
        Item.all_items.append(self)
    
    @classmethod
    def get_item(cls, item_name):
        for item in cls.all_items:
            if item.name == item_name:
                return item
        return None  # or raise an exception if the skill isn't found

def lesser_hp_potion_can_use(player):
    if player.chp == player.hp:
        input(f"{player.name} is already at full HP.")
        return False
    else:
        return True

def lesser_hp_potion_use(player):
    item_in_inventory = next((i for i in player.inv if i['name'] == 'Lesser HP Potion'), None)
    player.chp += 25
    if player.chp >= player.hp:
        player.chp = player.hp
        item_in_inventory['count'] -= 1
        if item_in_inventory['count'] <= 0:
            player.inv.remove(item_in_inventory)
        input(f"{player.name} had their HP fully restored!")
    else:
        input(f"{player.name} had their HP recovered by 25.")
    return True

items = [
    Item('Lesser HP Potion', 'Swirls of pink and light red inside. Heals 25 HP.', lesser_hp_potion_can_use, lesser_hp_potion_use)
]