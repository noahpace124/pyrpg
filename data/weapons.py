#Imports

class Weapon:
    all_weapons = []  # Class-level attribute to hold all weapon instances

    def __init__(self, name, desc, msg, atkmin, atkmax, matkmin, matkmax, req1a=None, req1m=0, req2a=None, req2m=0):
        self.name = name
        self.desc = desc
        self.msg = msg
        self.atkmin = atkmin
        self.atkmax = atkmax
        self.matkmin = matkmin
        self.matkmax = matkmax
        self.req1a = req1a
        self.req1m = req1m
        self.req2a = req2a
        self.req2m = req2m
        Weapon.all_weapons.append(self)  # Automatically add the instance to the class-level list

    def __repr__(self):
        return f"<Weapon(name={self.name}, atkmin={self.atkmin}, atkmax={self.atkmax})>"

    @classmethod
    def get_weapon(cls, weapon_name):
        for weapon in cls.all_weapons:
            if weapon.name == weapon_name:
                return weapon
        return None  # Return None if the weapon isn't found

# Example weapon instances
weapons = [
    Weapon('None', '', 'threw a punch', 0, 0, 0, 0),
    Weapon('Club', 'A crude wooden club.', 'swung their club', 0, 2, 0, 0, 'str', 2),
    Weapon('Rusty Sword', 'A rusty shortsword.', 'slashed their sword', 1, 2, 0, 0, 'str', 3),
    Weapon('Beginner\'s Staff', 'An easy to use staff for casting magic.', 'swung their staff', 0, 0, 0, 2, 'int', 2),
]