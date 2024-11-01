# Imports from Packages
import os
import inquirer

# Imports from Files
from helper import Helper
from data.races import races
from data.jobs import jobs
from data.player import Player

# Functions
def choose_name():
    Helper.clear_screen()
    print("Let's start with your name.")
    name = input(">> ")
    print(f"{name} is your name? (y/n)")
    ans = input(">> ").lower()
    if Helper.yes_or_no(ans) == 1:
        return name
    return choose_name()

def choose_race():
    Helper.clear_screen()  # Clear the screen at the start
    print("Next, what race are you?")

    questions = [
        inquirer.List('selected_race',
                      message="Please select a race",
                      choices=[race.name for race in races],  # Only display the race name
                      ),
    ]

    answer = inquirer.prompt(questions)

    # Extract the chosen race name from the answer
    chosen_race_name = answer['selected_race']

    # Find the chosen race object
    chosen_race = next(race for race in races if race.name == chosen_race_name)

    # Print the description before confirming
    print(f"{chosen_race.desc}")
    print(f"You are a {chosen_race_name}? (y/n)")
    ans = Helper.yes_or_no(input(">> ").lower())

    if ans == 1:
        return chosen_race  # Return the chosen race object

    return choose_race()  # Repeat the selection process if invalid


def choose_job():
    Helper.clear_screen()
    print("Finally, what class are you?")

    questions = [
        inquirer.List('selected_job',
                      message="Please select a job",
                      choices=[f"{job.name}" for job in jobs],
                      ),
    ]

    answer = inquirer.prompt(questions)

    # Extract the chosen job name from the answer
    chosen_job_name = answer['selected_job'].split(':')[0].strip()

    # Find the chosen job object
    chosen_job = next(job for job in jobs if job.name == chosen_job_name)

    # Confirm the chosen job
    print(f"{chosen_job.desc}")
    print(f"You are a {chosen_job_name}? (y/n)")
    ans = Helper.yes_or_no(input(">> ").lower())
    if ans == 1:
        for job in jobs:
            if job.name.lower() == chosen_job_name.lower():
                return job
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
    print("a place full of travelers trying to achieve their peaks...")
    print("and also full of unknown creatures ready to put you back in your place...")
    print("Your reason for coming may be a secret, but not all things can remain hidden...")
    input("(Press enter to continue...) ")

    name = choose_name()
    race = choose_race()
    job = choose_job()
    
    while True:
        Helper.clear_screen()
        print(f"You are {name} the {race.name} {job.name}? (y/n)")
        ans = input(">> ").lower()
        
        if Helper.yes_or_no(ans) == 1:
            player = create_player(name, race, job)  # Create the player instance
            return player
        elif Helper.yes_or_no(ans) == 0:
            return character_creation()
        elif Helper.yes_or_no(ans) == -1:
            input("Invalid answer. Try typing 'yes' or 'no'.")
