import os
import sys
import story
from util import slow_print

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
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
        self.ranged = False

class location():
    def __init__(self, name: str, accessible: bool):
        self.name = name
        self.key_item = " "
        self.has_access = accessible
        self.exit_to_location = None
        self.view = ""
        self.description = ""
        self.adjacent_locations = {}
        self.items_in_location = {}
        self.loc_lock_msg = "locked... need a key."
        self.limitor = "locked door"

class player():
    def __init__(self, start_location: location):
        self.hp = 100
        self.sanity = 100
        self.hunger = 0  # kind of like WOH's DOOM stat
        self.ailments = {}
        self.inventory = {}
        self.objectives = {"Check out the HOUSE and the GARAGE"}
        self.location = start_location
        self.prev_location = None
        self.game_over = False

# player interactivivty funcs

def quit_game():
    tf = input("Are you sure you want to quit? (Y/N): ")
    if (tf.lower() == "y") or (tf.lower() == "yes"):
        # add save mechanism
        sys.exit(2)

def go_to(current_player: player, destination: str):
    if current_player.location == destination:
        print("You are already there!")

    for loc in current_player.location.adjacent_locations:
        if (loc.name.lower() == destination) and loc.has_access:
            current_player.location = loc
            print(current_player.location.description)
            return
        elif (loc.name.lower() == destination) and (loc.has_access == False):
            print(loc.loc_lock_msg)
    print("Can't go to " + destination + "!")

def exit_location(current_player: player, current_location: str):
    if current_location == current_player.location.name.lower():
        if current_player.location.exit_to_location is not None:
            current_player.location = current_player.location.exit_to_location
        else:
            print("No clear exit!")
    else:
        print("Not in " + current_location)


def look_around(current_player: player):
    current_location = current_player.location
    print(current_location.view + "\n")

def unlock(current_player: player, loc_to_unlock: str):
    for loc in current_player.location.adjacent_locations:
        if (loc.name.lower() == loc_to_unlock) and (loc.has_access == False):
            loc.has_access = True
            print(loc.name + " is now accessible!")
            #print(loc.limiter + "is open!")

def list_inventory(current_player: player):
    print("ITEMS IN INVENTORY:")
    for item in current_player.inventory:
        print(item.name)

def prompt(player: player):
    inpt_string = input("> ").lower()
    cmd = inpt_string.split(" ")
    if cmd[0] == "look" and cmd[1] == "around":
        look_around(player)
    elif cmd[0] == "go" and cmd[1] == "to":
        go_to(player, cmd[2])
    elif (cmd[0] == "check" and cmd[1] == "inventory") or (cmd[0] == "backpack"):
        list_inventory(player)
    elif cmd[0] == "exit":
        try:
            exit_location(player, cmd[1])
        except IndexError:
            print("Where do you want to exit from?")
    elif cmd[0] == "unlock":
        unlock(player, cmd[1])
    else:
        print("I don't know what you want me to do.")


# instantiate items and give detail
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
truck.available_actions = typical_location_actions.add("exit")
truck.exit_to_location = driveway
truck.adjacent_locations = {driveway}
truck.view = "The cab of the truck suddenly feels too small. The drive didn't do your back any favors either.\nSnow is already starting to blanket the windshield. Time to exit the TRUCK."
truck.description = "Rot holes and an ever-present engine light. This truck has been 'on the way out' for years now."

#DRIVEWAY
driveway.available_actions = typical_location_actions
driveway.adjacent_locations = {house, garage}
driveway.view = story.driveway_view
driveway.description = story.driveway_desc


#HOUSE

#GARAGE








def start_game():
    os.system('clear')
    mainguy = player(truck)
    mainguy.inventory = {house_key, garage_key}

    print(story.prologue)
    while mainguy.game_over == False:
        #os.system('clear')
        line_len = len(mainguy.location.description)
        print("-" * line_len)
        print(mainguy.location.name)
        print(mainguy.location.description + "\n")
        print("-" * line_len)
        prompt(mainguy)




if __name__ == "__main__":
    title_screen()