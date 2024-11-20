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
        name='Human',
        desc='Humans are the most diverse race among them all. Humans find meaning in something and live for it and are not bound by traditions as much as others would be. Their only fault is that they tend to put themselves above all other races.',
        con=0, 
        mag=0, 
        str=1, 
        int=0, 
        dex=1, 
        lck=2, 
        df=0, 
        mdf=0
    ),
    Race(
        name='Kobold',
        desc='Kobolds are small reptilian creatures often explained as \'dragon dogs\'. Kobolds are swift and hold some physical resistance with their scales, but aren\'t adept at much else. They like to live in packs and are huge treasure seekers who love all things shiny.',
        con=0,
        mag=0,
        str=0,
        int=0,
        dex=2,
        lck=2,
        df=5,
        mdf=0
    ),
    Race(
        name='Xeran',
        desc='Xeran are extremely rare and powerful with magic. Xeran have the looks of a goat, but the figure of a human. Xeran females become mages while males become warriors that weave weapon and magic. They struggle to find a place among other races even though they fought for peace among all.',
        con=0, 
        mag=1, 
        str=0, 
        int=2, 
        dex=1, 
        lck=0, 
        df=0, 
        mdf=10
    )
]