class Armor:
    all_armors = []  # Class-level attribute to hold all armor instances

    def __init__(self, name, desc, df, mdf, reqa=None, reqm=0):
        self.name = name
        self.desc = desc
        self.df = df
        self.mdf = mdf
        self.reqa = reqa
        self.reqm = reqm
        Armor.all_armors.append(self)  # Automatically add the instance to the class-level list

    def __repr__(self):
        return f"<Armor(name={self.name}, df={self.df}, mdf={self.mdf})>"

    @classmethod
    def get_armor(cls, armor_name):
        for armor in cls.all_armors:
            if armor.name == armor_name:
                return armor
        return None  # Return None if the armor isn't found

# Example armor instances
armors = [
    Armor('None', '', 0, 0),
    Armor('Cloth', 'Simple cloth that covers the user.', 1, 0),
    Armor('Leather Armor', 'Sturdy leather armor with metal pieces built in.', 3, 0, 'str', 3),
    Armor('Robe', 'A cloth robe covered over the user that provides little defense.', 0, 2)
]