import universals as univ
import json
import time

def menu(account):
    menu_options = ["Display Inventory","Display Position","Other Info","Save","Exit"]
    while True:
        print("\n~~~MENU~~~\n")
        for i,value in enumerate(menu_options,1):
        	print(str(i)+". "+value)
        menu_input = int(input("\nEnter the corresponding number: >>"))
        if menu_options[menu_input-1] == "Display Inventory":
            disp_inventory()
        if menu_options[menu_input-1] == "Display Position":
            disp_position()
        if menu_options[menu_input-1] == "Other Info":
            other_info()
        if menu_options[menu_input-1] == "Save":
            player.save()
        if menu_options[menu_input-1] == "Exit":
            break

def disp_inventory():
    print("\n~~~YOUR INVENTORY~~~\n")
    for key in player.inventory:
        print(univ.ListOfItems[key].description +": " + str(player.inventory[key]))

def disp_position():
    print("\n~~~YOUR POSITION~~~\n"
        "Position:" + player.position)

def other_info():
    print("\n~~~OTHER INFO~~~\n"
        "\nCreate Time: %s"
        "\nLast Login Time: %s" 
        "\nExperience: %s" % (time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(player.createtime)), time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(player.lastlogin)), player.exp['fishing']))

def save():
    print("\nSaving...\n")
    stats = {
    "username": player.username,
    "password": player.password,
    "createtime": player.createtime,
    "lastlogin": player.lastlogin,
    "exp": player.inventory,
    "inventory": player.inventory,
    "position": player.position
    }
    with open('./PlayerAccts/'+player.username+'_p.json', 'w') as file:
        json.dump(stats, file)    
    print("Save complete.")

def exit():
    print("\nExiting program...")

if __name__ == "__main__":
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(reader['username'], reader['password'], reader['createtime'], reader['lastlogin'], reader['exp'], reader['inventory'], reader['position'])
    menu(player)