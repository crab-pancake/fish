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
    def __init__(self,code,name,description,travel):
        self.code = code
        self.name = name
        self.description = description
        self.places = {0:('Leave', travel)}
        with open('./locations/'+self.code+'_l.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                i=1
                if row['type'] == 'shop':
                    self.places[i] = (row['name'], Shop(row['code'],row['name'],row['desc'],row['type'],row['introline'],row['exitline']))
                elif row['type'] == 'FishSpot':
                    self.places[i] = (row['name'], FishSpot(row['code'],row['name'],row['desc'],row['type'],row['min_level']))
                i+=1
        self.destinations = travel.split(';')
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass

class Place(object):
    def __init__(self,code,name,description,Type):
        self.code = code
        self.name = name
        self.description = description
        self.actions = {1:('Do something',self.dosomething), 2:('Talk to the owner',self.talk), 0:('Leave', self.leave)}
    def takeaction(self,player):
        while True:
            print("\nameWhat do you want to do?")
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
    def __init__(self, code, name,description,Type, IntroLine, ExitLine):
        super().__init__(code,name,description,Type)
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
    def __init__(self,code,name,description,Type,skill,reqEquip,reqMats,min_level,successline,failline):
        super().__init__(code,name,description,Type)
        self.min_level=min_level
        self.skill=skill
        self.reqEquip=reqEquip
        self.reqMats=reqMats #reqMats will be a dict
        self.loottable='./tables/'+code+'_t.csv'
        self.successline=successline
        self.failline=failline
    def TrainSkill(self, player):
        if player.exp[self.skill] < self.min_level: #*univ.levelmult
            print("Your [ %s ] level isn't high enough to work here.\n"
                "The minimum level for this spot is %s, your level is [ %s ]."%(self.skill,self.min_level,player.exp[self.skill]))#exp must be divided by levelmult eventually
            #return something? (player, )
        else:
            with open(self.loottable,'r') as file:
                reader=dict(csv.reader(file))
                while True:
                    choice=input("Do you want to work here? (Y/N)\n>> ").strip().lower()
                    if choice in univ.yes:
                        enoughStuff=True
                        for item in reqMats:
                            if player.inventory[item] < reqMats[item]:
                                enoughStuff=False
                                print("You don't have enough [ %s ].\n"
                                      "Required: %s\n"
                                      "Your inventory: %s"%(univ.ListOfItems[item].name, reqMats[item],player.inventory[item]))
                                return (player,displayPlaces)
                        if enoughStuff:
                            success=False
                            rng=random.randint(1000)
                            for item in reader:
                                if rng>=int(reader[item]):
                                    success=True
                                    player.inventory[item]+=1
                                    print(self.successline(player,key))
                                    print("You gained [ %s ] %s experience. "%(univ.ListOfItems[item].exp,self.skill))
                                    # Possibly add another part for lucky items? Chests, extra fish, etc. 
                                    break
                            if not success:
                                print(self.failline)
                    else:
                        return (player,displayPlaces)

class FishSpot(Place):
    """Class for fishing spots."""
    def __init__(self,code,name,description,Type,min_level):
        self.skill='fishing'
        super().__init__(code,name,description,Type)#skill,reqMats,min_level,successline,failline
        self.min_level = min_level
        self.loottable = './tables/'+code+'_t.csv'
        self.reqMats="reqMats"
        self.failline=""
        self.actions[3] = ("Fish!", self.StartFishing) #self.TrainSkill
        # self.weather = weather  # add this later
    def successline(self,player,item):
        return "You successfully caught a %s!\nYou now have %s %s."%(univ.ListOfItems[item].name,player.inventory[item],univ.ListOfItems[item].name)
    def StartFishing(self, player):
        with open(self.loottable, 'r') as file:
            reader = dict(csv.reader(file))
            while True:
                fish = input("Would you like to fish? Press Y for yes, N for no.\n>> ").strip().lower()
                if fish in univ.yes:
                    if player.inventory['i00000'] >0:
                        player.inventory['i00000'] -= 1
                        rng = random.randint(1,100)
                        catch = False
                        for key in reader:
                            if rng >= int(reader[key]):
                                player.inventory[key]+=1
                                print('You caught a [',univ.ListOfItems[key].item_name,'] .')
                                print("You have",player.inventory[key],univ.ListOfItems[key].item_name+'.')
                                player = self.suc_fish(player,univ.ListOfItems[key].exp)
                                print("You got %s exp. " % (univ.ListOfItems[key].exp))
                                catch = True
                                break
                        if catch == False:
                            print("You didn't catch anything.")
                            player = self.suc_fish(player,0)
                    else: print ("You have no fishing juice left. Try waiting at least another hour.")
                elif fish in univ.no: 
                    return (player, self.takeaction)
                    break
                else:  univ.error(2)
    def suc_fish(self,player,fish_exp):
        print ("You have",player.inventory['i00000'],"fishing juice remaining.")
        player.exp['fishing'] += fish_exp
        player.save()
        return player

Locations = {}

with open('locations_l.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        location = Location(*args)
        Locations[row['code']] = location

if __name__ == "__main__":
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(**reader)
    Locations[player.position].displayplaces(player)