#Import

class Item:
    def __init__(self, name, desc, func):
        self.name = name
        self.desc = desc
        self.func = func

def lesser_hp_potion(player):
    if player.chp == player.hp:
        return False
    player.chp += 25
    if player.chp >= player.hp:
        player.chp = player.hp
        print(f"{player.name}'s HP was fully restored!")
    else:
        print(f"{player.name}'s HP recovered by 25.")
    input()
    return True

items = [
    Item('Lesser HP Potion', 'Swirls of almost pink and light red inside. Heals 25 HP.', lesser_hp_potion)
]