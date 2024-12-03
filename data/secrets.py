#Imports
from data.dungeons.barrens import secret_barrels, secret_chest


class Secret_Interactable:
    all_secret_interactables = []

    def __init__(self, name, desc, func, locations):
        self.name = name
        self.desc = desc
        self.func = func
        self.locations = locations
        Secret_Interactable.all_secret_interactables.append(self)

        self.blocks = None

    @classmethod
    def get_secret_interactables_by_location(cls, location):
        interactables = []
        for interactable in cls.all_secret_interactables:
            if location in interactable.locations:
                interactables.append(interactable)
        return interactables


class Secret:
    all_secrets = []

    def __init__(self, name, desc, func, locations):
        self.name = name
        self.desc = desc
        self.func = func
        self.locations = locations
        Secret.all_secrets.append(self)
    
    @classmethod
    def get_secrets_by_location(cls, location):
        secrets = []
        for secret in cls.all_secrets:
            if location in secret.locations:
                secrets.append(secret)
        return secrets


secret_interactables = [
    Secret_Interactable(
        name="Barrels",
        desc="There are some wooden barrels here. There might be something inside.",
        func=secret_barrels,
        locations=["barrens"]
    )
]

secrets = [
    Secret(
        name="Secret Chest",
        desc="A room with a secret treasure chest!",
        func=secret_chest,
        locations=["barrens"]
    )
]
