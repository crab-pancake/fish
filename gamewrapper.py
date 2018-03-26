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

def looper(player):
    choice=input("What do you want to do?")
    # Display the different menu options here: 
    # Change password, change equipment, view news

def relog(p):
    MultDict={"i00000":0} # fromkeys(items which regen over time,0)
    for slot in p.equipment:
        if p.equipment[slot]:
            for item,pct in univ.Items[p.equipment[slot]].equipeffects['login'].items():
                MultDict[item] += pct
                print("Your %s gives you %s percent more %s per hour."
                    %(univ.Items[p.equipment[slot]].name,pct*100,univ.Items[item].name))
    for item,pct in MultDict.items():
        p.inventory[item]+=min(99,int(p.hsll*(1+pct))) # 1+pct changes to base_rate*(1+pct)

def start_acct(uname):
    with open('./PlayerAccts/'+uname+'_p.json', 'r') as file:
        reader = json.load(file)
        player = univ.Player(**reader)
        import moderating
        moderating.update(player.username)
        if player.lastlogin == 0: # If this is the first access of the game, then lastlogin == 0
            print('running first mode') #for debug purposes
            player.updatetime()
            player.inventory = dict.fromkeys(univ.Items,0)
            player.inventory['i00000'] += 10  # when account is created, 10 fishing juice is given
            player.save()
            print("Welcome to the game, %s! This is your first login.\nAccount creation time: %s"
                %(player.username, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(player.createtime))))
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
                  %(player.username, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(player.createtime)), int(player.hsll), int((player.hsll*60)%60), int(player.hsll)))
            mover(player)

        elif player.lastlogin - player.createtime < 0:
            print("Error happened.")

def main():
    with open('./PlayerAccts/test_acct_p.json', 'w') as file:
        stats = {"username":"test_acct", "password":"","createtime":time.time(),"lastlogin":0,"exp":dict.fromkeys(univ.skills,0),
                 "inventory":dict.fromkeys(univ.Items,0),"position": "000", "equipment":dict.fromkeys(range(1,10),None),"bank":{}}
        json.dump(stats, file)
    start_acct('test_acct')

if __name__ == "__main__":
    main()