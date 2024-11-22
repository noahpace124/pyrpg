# Imports
from helper import Helper
from data.races import races
from data.jobs import jobs
from data.player import Player

# Functions
def choose_name():
    Helper.clear_screen()
    print("Let's start with your name.")
    name = input(">> ")
    if len(name.strip()) == 0:
        input("Invalid Name: Name must be made of characters.")
        return choose_name()
    name = Helper.string_color(name, 'y')
    print()
    print(f"{name} is your name? (y/n)")
    answer = Helper.yes_or_no()
    if answer == 1:
        return name
    elif answer == 0:
        return choose_name()

def choose_race():
    Helper.clear_screen()
    print("Next, what race are you?")

    answer = Helper.prompt([race.name for race in races])

    # Extract the chosen race name from the answer
    chosen_race_name = [race.name for race in races][answer]

    # Find the chosen race object
    chosen_race = next(race for race in races if race.name == chosen_race_name)

    print()

    # Print the description before confirming
    print(f"{chosen_race.desc}")
    print(f"You are a {chosen_race_name}? (y/n)")
    ans = Helper.yes_or_no()

    if ans == 1:
        return chosen_race  # Return the chosen race object
    elif ans == 0:
        return choose_race()


def choose_job():
    Helper.clear_screen()
    print("Finally, what background are you?")

    answer = Helper.prompt([job.name for job in jobs])

    # Extract the chosen job name from the answer
    chosen_job_name = [job.name for job in jobs][answer]

    # Find the chosen job object
    chosen_job = next(job for job in jobs if job.name == chosen_job_name)

    print()

    # Confirm the chosen job
    print(f"{chosen_job.desc}")
    print(f"You are a {chosen_job_name}? (y/n)")
    ans = Helper.yes_or_no()

    if ans == 1:
        return chosen_job  # Return the chosen race object
    elif ans == 0:
        return choose_job()

def create_player(name, race, job):
    return Player(  # Return the created player instance
        name,
        race,  # Use race name
        job,   # Use job name
        'barrens'
    )

def character_creation():
    Helper.clear_screen()
    print("You are approaching the land of Zenith:")
    print("a place full of travelers trying to grow one way or another,")
    print("a place full of monsters ready to humble any over eager adventurer,")
    print("and a place surrounded with mysterious treasures waiting to be uncovered.")
    input("Your reason for traveling here may be a secret, but some things need to be made clear...")

    name = choose_name()
    race = choose_race()
    job = choose_job()
    
    while True:
        Helper.clear_screen()
        print(f"You are {name} the {race.name} {job.name}? (y/n)")
        answer = Helper.yes_or_no()
        
        if answer == 1:
            player = create_player(name, race, job)  # Create the player instance
            return player
        elif answer == 0:
            return character_creation()
