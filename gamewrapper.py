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
        else:
            myTuple=nextAction
    return player

def start_acct(uname):
    with open('./PlayerAccts/'+uname+'_p.json', 'r') as file:
        reader = json.load(file) # This returns a dictionary with all the information in it. 
        player = univ.Player(**reader)
        from moderating import update
        update(uname)
        if player.lastlogin == 0: # If this is the first access of the game, then ptimeraw == 0
            print('running first mode') #for debug purposes
            player.updatetime()
            player.inventory = dict.fromkeys(univ.ListOfItems, 0)
            player.inventory['i00000'] = 10  #when account is created, 10 fishing juice is given
            player.save()
            print ("Welcome to the game, %s! This is your first login. \n"
                   "Account creation time: %s"% (player.username, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(player.createtime))))
            mover(player)

        elif player.lastlogin - player.createtime > 0: 
            print('running second mode') #for debug purposes
            player.updatetime()
            player.relog()
            player.save()
            print ("___________________\n"
                   "Welcome back to the game, %s!\n"
                   "Account creation time: %s\n"
                   "Time since last login: %s hrs, %s mins\n\n"
                   "You've acquired [ %s ] unit(s) of fishing juice since the last login. \n"   
                   "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n" 
                   %(player.username, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(player.createtime)), int(player.hsll), int(player.hsll%60), int(player.hsll)))
            mover(player)

        elif player.lastlogin - player.createtime < 0:
            print("Error happened.")

if __name__ == "__main__":
    with open('./PlayerAccts/test_acct_p.json', 'w') as file:
        stats = {"username": "test_acct", "password": "","createtime": time.time(),"lastlogin": 0,
            "exp": {"fishing": 0},"inventory": {},"position": "000", "equipment":{}}
        json.dump(stats, file)
    start_acct('test_acct')

