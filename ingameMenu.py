import universals as univ
import json
import time

def menu(player):
    menu_options = {1:("Display Inventory",disp_inventory), 2:("Display Position",disp_position), 3:("Other Info",other_info), 4:("Save",save), 5:("Return to game",return_to_game), 0:("Exit Game",exit)}
    while True:
        print("\n~~~MENU~~~\n")
        for key in menu_options:
            print(str(key)+". "+menu_options[key][0])
        print("\nEnter the corresponding number:\n")
        choice = univ.IntChoice(len(menu_options),[],[0])
        var = menu_options[choice][1](player)
        if var:
            return var

def disp_inventory(player):
    print("\n~~~YOUR INVENTORY~~~\n")
    for key in player.inventory:
        print(univ.ListOfItems[key].description +": " + str(player.inventory[key]))

def disp_position(player):
    print("\n~~~YOUR POSITION~~~\n"
        "Position:" + player.position)

def other_info(player):
    print("\n~~~OTHER INFO~~~\n"
        "\nCreate Time: %s"%(time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(player.createtime)),)
        "\nLast Login Time: %s"%(time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(player.lastlogin)),)
        "\nExperience: %s"%(player.exp['fishing']))

def save(player):
    print('saved')
    player.save()

def exit(player):
    print("\nExiting program...")
    import gamemap.quit
    return (player, gamemap.quit)

def return_to_game(player):
    print("\nReturning to game...")
    return (player,"prev")

if __name__ == "__main__":
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(reader['username'], reader['password'], reader['createtime'], reader['lastlogin'], reader['exp'], reader['inventory'], reader['position'])
    menu(player)