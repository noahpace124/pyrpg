#Import
from data.dungeons.barrens import abandoned_sack, abandoned_barrels

class Interactable:
    all_interactables = []

    def __init__(self, name, locations, desc, func, chance=50):
        self.name = name
        self.locations = locations
        self.desc = desc
        self.func = func
        self.chance = chance
        Interactable.all_interactables.append(self)

    def __repr__(self):
        return self.name

    @classmethod
    def get_interactables_by_location(cls, location):
        interactables = []
        for interactable in cls.all_interactables:
            if location in interactable.locations:
                interactables.append(interactable)
        return interactables
    

interactables = [
    Interactable(
        name="Sack",
        locations=["barrens"],
        desc="There is a sack on the ground. It appears to be moist with a weird liquid.",
        func=abandoned_sack,
        chance=100
    ),
    Interactable(
        name="Barrels",
        locations=["barrens"],
        desc="There are some wooden barrels here. There might be something inside.",
        func=abandoned_barrels,
        chance=100
    )
]