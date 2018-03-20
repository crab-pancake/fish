import universals as univ
import json
import time

def menu(player):
    menu_options = {1:("Display Inventory",disp_inv),2:("Display Position",disp_pos),3:("Other Info",info),4:("Save",save),5:("Back to game",back),6:("Help", helptext),7:("Equipment",eqptMenu),0:("Exit Game",exit)}
    while True:
        print("\n~~~MENU~~~\n")
        for key in menu_options:
            print(str(key)+". "+menu_options[key][0])
        print("\nEnter the corresponding number:\n")
        choice = univ.IntChoice(len(menu_options),['x'],[0])
        if choice=='x':
            return (player,"prev")
        var = menu_options[choice][1](player)
        if var:
            return var

def disp_inv(player):
    print("\n~~~YOUR INVENTORY~~~\n")
    for key in player.inventory:
        print(univ.ListOfItems[key].name +": " + str(player.inventory[key]))
        print("   "+univ.ListOfItems[key].desc)

def disp_pos(player):
    from gamemap import Locations
    print("\n~~~YOUR POSITION~~~\n"
        "Position: "+Locations[player.position].name)

def info(player):
    print("\n~~~OTHER INFO~~~\n"
        "\nCreate Time: %s"
        "\nLast Login Time: %s"
        "\nExperience: %s"%(time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(player.createtime)),time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(player.lastlogin)),player.exp['fishing']))

def save(player):
    player.save()
    print('saved')

def exit(player):
    from gamemap import quit
    return player,quit

def helptext(player):
    print("""\n~~~HELP~~~
    ----------------------------
    History:
    Jerry and Dayu thought of this game as they were walking with Evan and Mummy, along Lake Nordenskjoeld, W-Trek, Patagonia, Chile in late December 2017. 
    The inspiration came from many hours of idle chat, but at least it encouraged them to do something productive!

    Aim:
    This is a time based game, where you as the player character gather 'fishing juice' to catch fish, upgrade your setup and further your fishing capabilities.

    Initial setup:
    You'll begin with 10 fishing juice and no fish. Under the 'Menu' option, choose 'Fish!' to use up your fishing juice and catch fish.
    Each time you'll have a go at fishing and deplete your fishing juice by one. 
    You'll gather more fishing juice by logging off (1 per hour is the base rate) and relogging on.

    Buying and selling:
    Enter the corresponding number 'Visit shop' in order to buy and sell your fish to gain gold. Use your gold to upgrade your fishing set up. 
    For example, the cheapest upgrade will is the 'Reinforced net', which will increase your fishing juice gathering rate by 10%.

    Final words:
    Good luck! We'll be slowly adding in extra features, but be patient as we are new :3""")

def back(player):
    print("\nReturning to game...")
    return player,"prev"

def eqptMenu(player):
    while True:
        print("\nCurrently equipped:")
        for slot in player.equipment:
            if player.equipment[slot]:
                print("Slot %s: %s"%(slot,univ.ListOfItems[player.equipment[slot]].name))
        print("\nEquipment in your inventory:")
        alleqpt=[]
        for item in player.inventory:
            try:
                if univ.ListOfItems[item].slot and player.inventory[item]:
                    alleqpt.append(item)
            except AttributeError as e:
                pass
        for num,item in enumerate(alleqpt,1):
            print(num,univ.ListOfItems[item].name,player.inventory[item])
        print("x Return")
        print("Which item do you want to equip?")
        choice=univ.IntChoice(len(alleqpt),["x"],[])
        if choice=="x":
            return
        else:
            player.equip(univ.ListOfItems[alleqpt[choice-1]])
            player.save()


if __name__ == "__main__":
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(**reader)
    menu(player)