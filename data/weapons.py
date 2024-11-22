#Imports

class Weapon:
    all_weapons = []  # Class-level attribute to hold all weapon instances

    def __init__(self, name, desc, msg, atkmin, atkmax, matkmin, matkmax, stat, req1a=None, req1m=0, req2a=None, req2m=0):
        self.name = name
        self.desc = desc
        self.msg = msg
        self.atkmin = atkmin
        self.atkmax = atkmax
        self.matkmin = matkmin
        self.matkmax = matkmax
        self.stat = stat
        self.req1a = req1a
        self.req1m = req1m
        self.req2a = req2a
        self.req2m = req2m
        Weapon.all_weapons.append(self)  # Automatically add the instance to the class-level list

    @classmethod
    def get_weapon(cls, weapon_name):
        for weapon in cls.all_weapons:
            if weapon.name == weapon_name:
                return weapon
        return None  # Return None if the weapon isn't found

# Example weapon instances
weapons = [
    Weapon('None', '', 'threw a punch', 0, 0, 0, 0, 'str'),
    Weapon('Club', 'A crude wooden club.', 'swung their club', 0, 2, 0, 0, 'str', 'str', 2),
    Weapon('Wooden Staff', 'A simple wooden staff for basic magic.', 'swung their staff', 0, 1, 0, 1, 'str', 'int', 2),
    Weapon('Sling', 'A sling made from cloth to fire small pebbles.', 'slung a rock', 0, 1, 0, 0, 'dex', 'dex', 2),
    Weapon('Dagger', 'A simple iron dagger.', 'stabbed with their dagger', 0, 2, 0, 0, 'dex', 'dex', 2),
    Weapon('Rusty Sword', 'A rusty shortsword.', 'slashed their sword', 1, 2, 0, 0, 'str', 'str', 3),
    Weapon('Beginner\'s Staff', 'An easy to use staff for casting magic.', 'swung their staff', 0, 1, 0, 2,'str', 'int', 2),
]