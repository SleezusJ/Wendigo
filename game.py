import os
import sys

"""
TO-DO:
> settle on methods for unlocking doors and player actions and eliminate duplication.
> Add a slowprint function for effect.
"""



def get_title_option():
    option = input("> ").lower()
    if option == "play":
        start_game()
    elif option == "help":
        print_help()
        get_title_option()
    elif option == "quit":
        sys.exit()
    else:
        print("pick a valid option!")
        get_title_option()

def print_help():
    print("//HELP ")
    print("WENDIGO is a text based game and uses the command prompt to get player input.")
    print("Typical actions look like: ")
    print("> look around")
    print("> go to <area>")
    print("> inspect <object>")
    print("> use <object>")
    print("> take <object>")

def title_screen():
    os.system('clear')
    print("########################################################")
    print("#  __      __                   .___.__                #")
    print("# /  \\    /  \\ ____   ____    __| _/|__| ____   ____   #")
    print("# \\   \\/\\/   // __ \\ /    \\  / __ | |  |/ ___\\ /  _ \\  #")
    print("#  \\        /\\  ___/|   |  \\/ /_/ | |  / /_/  >  <_> ) #")
    print("#   \\__/\\  /  \\___  >___|  /\\____ | |__\\___  / \\____/  #")
    print("#        \\/       \\/     \\/      \\/   /_____/          #")
    print("########################################################")
    print("#                   (  -PLAY-  )                       #")
    print("#                   (  -HELP-  )                       #")
    print("#                   (  -QUIT-  )                       #")
    print("########################################################")
    get_title_option()

class item():
    def __init__(self, name: str, dur: int):
        self.name = name
        self.durability = dur
        self.ok_to_drop = False

class weapon(item):
    def __init__(self):
        self.damage = 0
        self.ranged = False

class door(item):
    def __init__(self):
        self.locked = True

class location():
    def __init__(self, name: str, accessible: bool):
        self.name = name
        self.key_item = ""
        self.has_access = accessible
        self.view = ""
        self.description = ""
        self.available_actions = {}
        self.adjacent_locations = {}
        self.items_in_location = {}


    def __access(self, attempted_key: item):
        if self.has_access:
            print("you already have access to " + self.name + "!")
        elif self.has_access is False and attempted_key.name == self.key_item:
            self.has_access = True
            print("You can now access " + self.name + "!")
        elif self.has_access is False and attempted_key.name != self.key_item:
            print("You need the " + self.key_item + " to get in here!")

class player():
    def __init__(self, start_location: location):
        self.hp = 100
        self.sanity = 100
        self.hunger = 0  # kind of like WOH's DOOM stat
        self.ailments = {}
        self.inventory = {}
        self.objectives = {"Check out the HOUSE and the GARAGE"}
        self.location = start_location
        self.game_over = False

# player interactivivty funcs

def quit_game():
    tf = input("Are you sure you want to quit? (Y/N): ")
    if (tf.lower() == "y") or (tf.lower() == "yes"):
        # add save mechanism
        sys.exit(2)

def go_to(current_player: player, destination: str):
    current_location = current_player.location
    for loc in current_location.adjacent_locations:
        if loc.name.lower() == destination.lower():
            current_player.location = loc
            print(current_player.location.description)
            return
    print("Can't go to " + destination + "!")

def look_around(current_player: player):
    current_location = current_player.location
    print(current_location.view)

def prompt():
    inpt_string = input("> ")

#instantiate items and give detail
house_key = item("HOUSE key", 1)
garage_key = item("GARAGE key", 1)
pvc_bow = weapon("PVC bow", 100)
pvc_bow.ranged = True


# instantiate locations and give detail
house = location("HOUSE", False)
garage = location("GARAGE", False)
driveway = location("DRIVEWAY", True)
truck = location("TRUCK", True)

typical_location_actions = {"look around", "inspect"}

#TRUCK
truck.available_actions = typical_location_actions + {"exit"}
truck.adjacent_locations = {driveway}
truck.view = "The cab of the truck suddenly feels too small. The drive didn't do your back any favors either.\nSnow is already starting to blanket the windshield.\nTime to exit the TRUCK."
truck.description = "Rot holes and an ever-present engine light.\nThis thing has been 'on the way out' for years."

#DRIVEWAY
driveway.available_actions = typical_location_actions
driveway.adjacent_locations = {house, garage}
driveway.view = "The GARAGE is in front of you and the adjoining HOUSE, off to the left."

#HOUSE

#GARAGE








def start_game():


    mainguy = player(truck)
    while mainguy.game_over == False:
        prompt()




if __name__ == "__main__":
    title_screen()