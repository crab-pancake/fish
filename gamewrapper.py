import json, time
import universals as univ
import gamemap as gmap

def mover(player):
    nextAction = gmap.displayPlaces
    while True:
        returned = nextAction(player) # returned will be a tuple of (playerObject, player'sNextAction)
        if returned==None:
            nextAction='prev'
        else:
            player = returned[0]
            prevAction=nextAction
            nextAction = returned[1]
        player.save()
        if nextAction == None:
            break
        elif nextAction=="prev":
            nextAction=prevAction
    return player

def relog(player):
    FJmult=0
    if player.equipment[1]:
        print("You have a %s. This gives you %s percent more fishjuice."%(univ.ListOfItems[player.equipment[1]].name,0))
    player.inventory['i00000']+=min(99,int(player.hsll))*(1+FJmult)

def start_acct(uname):
    with open('./PlayerAccts/'+uname+'_p.json', 'r') as file:
        reader = json.load(file)
        player = univ.Player(**reader)
        if player.lastlogin == 0: # If this is the first access of the game, then lastlogin == 0
            print('running first mode') #for debug purposes
            player.updatetime()
            player.inventory = dict.fromkeys(univ.ListOfItems,0)
            player.inventory['i00000'] += 10  # when account is created, 10 fishing juice is given
            player.save()
            print("Welcome to the game, %s! This is your first login.\n"
                  "Account creation time: %s"%(player.username, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(player.createtime))))
            mover(player)

        elif player.lastlogin-player.createtime>0: 
            print('running second mode') #for debug purposes
            player.updatetime()
            relog(player)
            player.save()
            print("___________________\n"
                  "Welcome back to the game, %s!\n"
                  "Account creation time: %s\n"
                  "Time since last login: %s hrs, %s mins\n\n"
                  "You've acquired [ %s ] unit(s) of fishing juice since the last login.\n"   
                  "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n" 
                  %(player.username, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(player.createtime)), int(player.hsll), int(player.hsll%60), int(player.hsll)))
            mover(player)

        elif player.lastlogin - player.createtime < 0:
            print("Error happened.")


if __name__ == "__main__":
    with open('./PlayerAccts/test_acct_p.json', 'w') as file:
        stats = {"username":"test_acct", "password":"","createtime":time.time(),"lastlogin":0,
            "exp":dict.fromkeys(univ.skills,0),"inventory":dict.fromkeys(univ.ListOfItems,0),"position": "000", "equipment":dict.fromkeys(range(1,10),None)}
        json.dump(stats, file)
    start_acct('test_acct')
