class Race:
    all_races = []  # Class-level attribute to hold all race instances

    def __init__(self, name, desc, con, mag, str, int, dex, lck, df, mdf):
        self.name = name
        self.desc = desc
        self.con = con
        self.mag = mag
        self.str = str
        self.int = int
        self.dex = dex
        self.lck = lck
        self.df = df
        self.mdf = mdf
        Race.all_races.append(self)  # Automatically add the instance to the class-level list

    def __repr__(self):
        return f"<Race(name={self.name}, con={self.con}, mag={self.mag}, df={self.df}, mdf={self.mdf})>"

    @classmethod
    def get_race(cls, race_name):
        for race in cls.all_races:
            if race.name == race_name:
                return race
        return None  # Return None if the race isn't found

# Example race instances
races = [
    Race(
        'Human',
        'Humans are the most diverse race among them all. Humans find meaning in something and live for it and are not bound by traditions as much as others would be. Their only fault is that they tend to put themselves above all other races.',
        1, 1, 1, 1, 1, 2, 0, 0
    ),
    Race(
        'Xeran',
        'Xeran are extremely rare and powerful with magic. Xeran have the looks of a goat, but the figure of a human. Xeran females become mages while males become warriors that weave weapon and magic. They struggle to find a place among other races even though they fought for peace among all.',
        1, 2, 0, 2, 1, 0, 0, 10
    )
]