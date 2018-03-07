import csv
import json
import universals as univ
import random
import ingameMenu

def displayPlaces(player):
    with Locations[player.position] as pos:
        print("You are currently at %s." % (pos.name))
        while True:
            print("Which place do you want to go into?")
            for num, place in sorted(pos.places.items())[1:]:
                print(num, pos.places[num][0])
            print(0, pos.places[0][0])
            choice=univ.IntChoice(len(pos.places),['x','m', 'q'],[0])
            if choice == 'x' or choice == 0:
                return (player, travel)
            elif choice == 'q':
                print("Quitting...")
                return (player, quit)
            elif choice == 'm':
                action = ingameMenu.menu(player)
                # return (player, action)
            else: 
                return (player, pos.places[choice][1].takeaction)

def travel(player):
    with Locations[player.position] as pos:
        print("You are leaving %s."%(pos.name))
        traveller = {0:'Return'}
        print('Type the number of the town you want to travel to.')
        for location in sorted(pos.destinations):
            i=1
            traveller[i] = Locations[location].name
            i+=1
        for num, loc in sorted(traveller.items())[1:]:
            print(num, traveller[num])
        print(0,traveller[0])
        while True:
            choice=univ.IntChoice(len(traveller), ['x','m'], [0])
            if choice == 0 or choice == 'x':
                print('Returning to %s...'%(pos.name))
                return (player, displayPlaces)
            elif choice == 'q':
                print("Quitting...")
                return (player, quit)
            elif choice == 'm':
                action=ingameMenu.menu(player)
                if action:
                    return action
            else:
                player.position = sorted(pos.destinations)[choice-1]
                print('You have moved to %s.'%(pos.name))
                print(pos.description)
                return (player, displayPlaces)

def quit(player):
    answer = input("Are you sure you want to quit? Type yes to confirm, or anything else to cancel.\n>> ").strip().lower()
    if answer in univ.yes:
        print("Thanks for playing, see you again soon.")
        return (player, None)
    else:
        print("Cancelled, returning to game.")
        return (player, displayPlaces)

class Location(object):
    def __init__(self,code,name,description,travel,**kwargs):
        self.code = code
        self.name = name
        self.description = description
        self.places = {0:('Leave', travel)}
        with open('./locations/'+self.code+'_l.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                i=1
                if row['type'] == 'shop':
                    self.places[i] = (row['name'], Shop(**row))
                elif row['type'] == 'FishSpot':
                    self.places[i] = (row['name'], FishSpot(**row))
                i+=1
        self.destinations = travel.split(';')
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass

class Place(object):
    def __init__(self,code,name,description,**kwargs):
        self.code = code
        self.name = name
        self.description = description
        self.actions = {1:('Do something',self.dosomething), 2:('Talk to the owner',self.talk), 0:('Leave', self.leave)}
    def takeaction(self,player):
        while True:
            print("\nWhat do you want to do?")
            for key, val in sorted(self.actions.items())[1:]:
                print(key, val[0])
            print(0, self.actions[0][0])
            choice=univ.IntChoice(len(self.actions),['x','m','q'],[0])
            if choice == 'q':
                print("Quitting...")
                return (player, quit)
            elif choice == 'x' or choice == 0:
                return self.leave(player)
            elif choice == 'm':
                ingameMenu.menu(player)
            else:
                self.actions[choice][1](player) #the value corresponding to the choice key in self.actions, second entry (always a function), called with (player) as the parameter
    def dosomething(self, player):
        print('Something has been done.')
    def talk(self, player):
        print('Talking to owner...')
    def leave(self, player):
        print("Leaving...")
        return (player, displayPlaces)
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass

class Shop(Place):
    """Class for shops selling different things."""
    def __init__(self,code,name,desc,IntroLine,ExitLine,**kwargs):
        super().__init__(code,name,desc)
        self.intro = IntroLine
        self.exit = ExitLine
        self.actions[3] = ('Shop', self.shopfront)
        # with open(code+'_s.csv', 'r') as file:
            # pass
    def shopfront(self, player):
        print(self.intro)
        self.inv = player.inventory
        print("What would you like to do?\n"
              "1. Sell\n"
              "2. Buy\n"
              "3. Exit\n")
        while True:
            choice = univ.IntChoice(3, [], [])
            if choice == 1:
                self.sell()
            elif choice == 2:
                self.buy()
            elif choice == 3:
                print(self.exit)
                break
    def sell(self):
        print("you are selling")
    def buy(self):
        print("you are buying")

class TrainingSpot(Place):
    """Superclass for skill training spots"""
    def __init__(self,code,name,description,skill,reqEquip,reqMats,min_lvl,failline,action,**kwargs):
        super().__init__(code,name,description)
        self.min_lvl=int(min_lvl)
        self.skill=skill
        self.reqEquip=reqEquip
        self.reqMats={k:int(v) for k,v in (x.split(':') for x in (reqMats.strip("[]")).split(';'))} #Get a string of form [k1:v1;k2:v2] and turn it into a dict
        self.loottable='./tables/'+code+'_t.csv'
        self.failline=failline
        self.action=action
        self.actions[3] = (self.action.title()+"!", self.TrainSkill)
    def TrainSkill(self, player):
        if player.exp[self.skill] < self.min_lvl: #*univ.levelmult
            print("Your [ %s ] level isn't high enough to %s here.\n"
                "The minimum level for this spot is %s, your level is [ %s ]."%(self.skill,self.action,self.min_lvl,player.exp[self.skill]))#exp must be divided by levelmult eventually
            return (player, displayPlaces)
        else:
            with open(self.loottable,'r') as file:
                reader=dict(csv.reader(file))
                while True:
                    choice=input("Do you want to %s here? (Y/N)\n>> "%(self.action)).strip().lower()
                    if choice in univ.yes:
                        enoughStuff=True
                        for item in self.reqMats:
                            if player.inventory[item] < self.reqMats[item]:
                                enoughStuff=False
                                print("You don't have enough [ %s ].\n"
                                      "Required: %s\n"
                                      "Your inventory: %s"%(univ.ListOfItems[item].name, reqMats[item],player.inventory[item]))
                                return (player,displayPlaces)
                        if enoughStuff:
                            success=False# dropper(player,self.loottable)
                            rng=random.randint(0,100)
                            for item in reader:
                                if rng>=int(reader[item]):
                                    success=True
                                    player.inventory[item]+=1
                                    print(self.successline(player,item))
                                    print("You gained [ %s ] %s experience. "%(univ.ListOfItems[item].exp,self.skill))
                                    # Possibly add another part for lucky items? Chests, extra fish, etc. 
                                    break
                            for item in self.reqMats:
                                player.inventory[item] -= self.reqMats[item]
                                print("You have [ %s ] %s remaining."%(player.inventory[item],univ.ListOfItems[item].name))
                            player.save()
                            if not success:
                                print(self.failline)
                    elif choice in univ.no:
                        return (player,displayPlaces)
                    else: univ.error(0)

class FishSpot(TrainingSpot):
    """Class for fishing spots."""
    def __init__(self,code,name,desc,reqEquip,reqMats,min_lvl,**kwargs):
        self.skill='fishing'
        self.failline="You didn't manage to catch anything."
        self.action="fish"
        super().__init__(code,name,desc,self.skill,reqEquip,reqMats,min_lvl,self.failline,self.action)
        # self.weather = weather  # add this later
    def successline(self,player,item):
        return "You successfully caught a %s!\nYou now have %s %s."%(univ.ListOfItems[item].name,player.inventory[item],univ.ListOfItems[item].name)
    def suc_fish(self,player,fish_exp):
        print ("You have",player.inventory['i00000'],"fishing juice remaining.")
        player.exp['fishing'] += fish_exp
        player.save()
        return player

Locations = {}

with open('locations_l.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        location = Location(row['code'], row['name'], row['description'], row['travel'])
        Locations[row['code']] = location

if __name__ == "__main__":
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(**reader)
    nextAction = displayPlaces
    while True:
        returned = nextAction(player)
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