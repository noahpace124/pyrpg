class Skill:
    all_skills = []  # Class-level attribute to hold all skill instances

    def __init__(self, name, desc, skill_type, cost, reqa, reqm, reta, func=None, when='turn'):
        self.name = name
        self.desc = desc
        self.type = skill_type  # 'type' renamed to 'skill_type' to avoid confusion
        self.cost = cost
        self.reqa = reqa
        self.reqm = reqm
        self.reta = reta
        self.func = func  # Add a reference to the skill function
        Skill.all_skills.append(self)  # Automatically add the instance to the class-level list

    def __repr__(self):
        return (f"<Skill(name={self.name}, desc={self.desc}, cost={self.cost}, "
                f"reqa={self.reqa}, reqm={self.reqm}, reta={self.reta}, skill_func={self.skill_func})>")

    @classmethod
    def get_skill(cls, skill_name):
        for skill in cls.all_skills:
            if skill.name == skill_name:
                return skill
        return None  # or raise an exception if the skill isn't found

# Define skill functions
def instant_recharge(player):
    player.ctp -= 8  # Use the cost directly, or you could get it from the skill instance
    player.cmp += player.int * 4
    if player.cmp >= player.mp:
        player.cmp = player.mp
        print(f"{player.name}'s MP recharged fully!")
    else:
        print(f"{player.name}'s MP recharged some.")
    input("(Press enter to continue...) ")

def heavy_blow(player):
    player.ctp -= 10  # Use the cost directly
    atk = player.get_atk()  # Assuming you have a method to get attack value
    add = player.str
    res = int(add * 1.5)
    return atk + (res * 2)

# Create skill instances
skills = [
    Skill(
        name='Instant Recharge',
        desc='Recharge some MP to use.',
        skill_type='buff',
        cost=8,
        reqa='int',
        reqm=3,
        reta=False,
        func=instant_recharge
    ),
    Skill(
        name='Heavy Blow',
        desc='Strike with concentrated effort. Use 1.5 times your str on this attack.',
        skill_type='atk',
        cost=10,
        reqa='str',
        reqm=3,
        reta=True,
        func=heavy_blow
    )
]