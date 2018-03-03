import universals as univ
import json

def menu(account):
    while True:
        print("This is a menu")
        break

if __name__ == "__main__":
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(reader['username'], reader['password'], reader['createtime'], reader['lastlogin'], reader['exp'], reader['inventory'], reader['position'])
    menu(player)
