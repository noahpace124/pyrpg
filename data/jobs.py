#Imports

#Imports from File
from .spells import Spell
from .skills import Skill
from .weapons import Weapon
from .armors import Armor

class Job:
    all_jobs = []  # Class-level attribute to hold all job instances

    def __init__(self, name, desc, con, mag, str, int, dex, lck, weapon, armor, spells, skills):
        self.name = name
        self.desc = desc
        self.con = con
        self.mag = mag
        self.str = str
        self.int = int
        self.dex = dex
        self.lck = lck
        self.weapon = weapon
        self.armor = armor
        self.spells = spells
        self.skills = skills
        Job.all_jobs.append(self)  # Automatically add the instance to the class-level list

    def __repr__(self):
        return f"<Job(name={self.name}, con={self.con}, mag={self.mag}, weapon={self.weapon}, armor={self.armor})>"

    @classmethod
    def get_job(cls, job_name):
        for job in cls.all_jobs:
            if job.name == job_name:
                return job
        return None  # Return None if the job isn't found

# Example job instances
jobs = [
    Job(
        name='Fighter',
        desc='Fighters excel in hand-to-hand combat with any weapon available to them.',
        con=4,
        mag=0, 
        str=4,
        int=0,
        dex=3, 
        lck=0, 
        weapon=Weapon.get_weapon('Rusty Sword'), 
        armor=Armor.get_armor('Leather Armor'), 
        spells=[], 
        skills=[Skill.get_skill('Damage Armor'), Skill.get_skill('Empowering Strike')]
    ),
    Job(
        name='Thief',
        desc='Thieves excel in agility and carry a great deal of luck with them.',
        con=2,
        mag=0,
        str=2,
        int=0,
        dex=4,
        lck=3,
        weapon=Weapon.get_weapon('Dagger'),
        armor=Armor.get_armor('Leather Armor'),
        spells=[],
        skills=[Skill.get_skill('Fast Attacks'), Skill.get_skill('Poison Stab')]
    ),
    Job(
        name='Wizard',
        desc='While not good at close combat, Wizards excel at all things magic and use it to overpower their enemies.',
        con=0,
        mag=5,
        str=0, 
        int=5,
        dex=1, 
        lck=0, 
        weapon=Weapon.get_weapon("Beginner's Staff"), 
        armor=Armor.get_armor('Robe'), 
        spells=[Spell.get_spell('Fireball')], 
        skills=[]
    )
]
