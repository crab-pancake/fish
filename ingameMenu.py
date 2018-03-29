import universals as univ
import json
import time

def menu(player):
    menu_options = {1:("Display Inventory",disp_inv),
        2:("Display Position",disp_pos),
        3:("Other Info",info),
        4:("Save",save),
        5:("Back to game",back),
        6:("Help", helptext),
        7:("Equipment",eqptMenu),
        0:("Exit Game",exit)}
    while True:
        print("\n"+"MENU".center(30,'=')+"\n")
        for key in menu_options:
            print(str(key)+". "+menu_options[key][0])
        print("\nEnter the corresponding number:\n")
        choice = univ.IntChoice(len(menu_options),['x'],[0])
        if choice=='x':
            return (player,"prev")
        var = menu_options[choice][1](player)
        if var:
            return var
        input("Press enter to continue.")

def disp_inv(player):
    print("\n"+"Your Inventory".center(24,'~')+'\n')
    for key in player.inventory:
        print((univ.Items[key].name+": ").ljust(15)+str(player.inventory[key]))
        print("   "+univ.Items[key].desc)

def disp_pos(player):
    from gamemap import Locations
    print("Your current position: "+Locations[player.position].name)

def info(player):
    print("\n"+"Other Info".center(24,'~')+"\n\nCreate Time: %s"
        "\nLast Login Time: %s\n\n===Experience==="
        %(time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(player.createtime)),
         time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(player.lastlogin))))
    for k,v in player.exp.items():
        print((k.title()+":").ljust(20),v)

def save(player):
    player.save()
    print('Your progress has been saved.')

def exit(player):
    from gamemap import quit
    return player,quit

def helptext(player):
    print("""\n~~~HELP~~~
    ----------------------------
    History:
    Jerry and Dayu thought of this game as they were walking with Evan and Mummy, along Lake Nordenskjoeld, W-Trek, Patagonia, Chile in late December 2017. 
    The inspiration came from many hours of idle chat, but at least it encouraged them to do somethiing productive!

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

slotnames=['Head','Arm 1','Arm 2','Body','Legs','Feet','Accessory 1','Accessory 2','Accessory 3']

def eqptMenu(player):
    options={1:"Equip items from inventory",2:"Unequip items",0:"Leave"}
    while True:
        print("\n===Currently equipped items===")
        for slot in player.equipment:
            if player.equipment[slot]:
                print("%s: %s"%(slotnames[slot-1],univ.Items[player.equipment[slot]].name))
            else:
                print("%s: None"%slotnames[slot-1])
        print("\nWhat would you like to do?")
        for option in options:
            print(option,options[option])
        choice=univ.IntChoice(len(options),[],[0])
        if choice==1:
            print("\nEquipment in your inventory:")
            alleqpt=[]
            for item in player.inventory:
                try:
                    if univ.Items[item].slot and player.inventory[item]:
                        alleqpt.append(item)
                except AttributeError as e:
                    pass
            for num,item in enumerate(alleqpt,1):
                print(num,univ.Items[item].name,player.inventory[item])
            print("x Return")
            print("Which item do you want to equip?")
            choice=univ.IntChoice(len(alleqpt),["x"],[])
            if choice=="x":
                return
            else:
                player.equip(univ.Items[alleqpt[choice-1]])
                player.save()
        elif choice==2:
            print("\n===Currently equipped items===")
            for slot in player.equipment:
                if player.equipment[slot]:
                    print("%s: %s"%(slotnames[slot-1],univ.Items[player.equipment[slot]].name))
            print("\nWhich slot do you want to unequip?")
            choice=univ.IntChoice(10,[],[0])
            if choice==0:
                return player,menu
            player.unequip(choice)
            player.save()
        elif choice==0:
            return player,menu

def main():
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(**reader)
    menu(player)

if __name__ == "__main__":
    main()