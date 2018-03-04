import csv
import json
import universals as univ
import random
import ingameMenu

def displayPlaces(player):
    print("You are currently at %s." % (Locations[player.position].name))
    while True:
        print("Which place do you want to go into?")
        for num, place in sorted(Locations[player.position].places.items())[1:]:
            print(num, Locations[player.position].places[num][0])
        print(0, Locations[player.position].places[0][0])
        choice=univ.IntChoice(len(Locations[player.position].places),['x','m', 'q'],[0])
        if choice == 'x' or choice == 0:
            return (player, travel)
        elif choice == 'q':
            print("Quitting...")
            return (player, quit)
        elif choice == 'm':
            action = ingameMenu.menu(player)
            print(action)
        else: 
            return (player, Locations[player.position].places[choice][1].takeaction)

def travel(player):
    print("You are leaving %s."%(Locations[player.position].name))
    traveller = {0:'Return'}
    print('Type the number of the town you want to travel to.')
    for location in sorted(Locations[player.position].destinations):
        i=1
        traveller[i] = Locations[location].name
    for num, loc in sorted(traveller.items())[1:]:
        print(num, traveller[num])
    print(0,traveller[0])
    while True:
        choice=univ.IntChoice(len(traveller), ['x','m'], [0])
        if choice == 0 or choice == 'x':
            print('Returning to old place... ')
            return (player, displayPlaces)
        elif choice == 'm':
            ingameMenu.menu(player)
        else:
            player.position = sorted(Locations[player.position].destinations)[choice-1]
            print('You have moved to %s.'%(Locations[player.position].name))
            print(Locations[player.position].description) # just testing
            return (player, displayPlaces)

def quit(player):
    answer = input("Are you sure you want to quit? Type yes to confirm, or anything else to cancel.\n>> ").strip().lower()
    if answer in['yes','ye','y']:
        print("Thanks for playing, see you again soon.")
        return (player, None)
    else:
        print("Cancelled, returning to game.")
        return (player, displayPlaces)

class Location(object):
    def __init__(self, code, name, description, travel):
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

class Place(object):
    def __init__(self, code, name, description,Type):
        self.code = code
        self.name = name
        self.description = description
        self.actions = {1:('Do something', self.dosomething), 2:('Talk to the owner', self.talk), 0:('Leave', self.leave)}
    def takeaction(self,player):
        print("What do you want to do?")
        while True:
            for key, val in sorted(self.actions.items())[1:]:
                print(key, val[0])
            print(0, self.actions[0][0])
            choice=univ.IntChoice(len(self.actions), ['x','m','q'],[0])
            if choice == 'q':
                print("Quitting...")
                return (player, quit)
            elif choice == 'x' or choice == 0:
                return self.leave(player)
            elif choice == 'm':
                ingameMenu.menu(player)
            else:
                self.actions[choice][1](player)
    def dosomething(self, player):
        print('Something has been done.')
    def talk(self, player):
        print('Talking to owner...')
    def leave(self, player):
        print("Leaving...")
        return (player, displayPlaces)

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

class FishSpot(Place):
    """Class for fishing spots."""
    def __init__(self,code,name,description,Type,min_level):
        super().__init__(code,name,description,Type)
        self.min_level = min_level
        self.loottable = './tables/'+code+'_t.csv'
        self.actions[3] = ("Fish!", self.StartFishing)
        # self.weather = weather  # add this later
    def StartFishing(self, player):
        with open(self.loottable, 'r') as file:
            reader = dict(csv.reader(file))
            while True:
                fish = input("Would you like to fish? Press Y for yes, N for no.\n>> ").strip().lower()
                if fish == "y":
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
                                print("You got %s exp" % (univ.ListOfItems[key].exp))
                                catch = True
                                break
                        if catch == False:
                            print("You didn't catch anything.")
                            player = self.suc_fish(player,0)
                    else: print ("You have no units of fishing juice left. Try waiting at least another hour.")
                elif fish == "n": 
                    return (player, self.takeaction)
                    break
                else:  univ.error(2)
    def suc_fish(self,player,fish_exp):
        print ("You have",player.inventory['i00000'],"fishing juice remaining.")
        player.exp['fishing'] += fish_exp
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
    player = univ.Player(reader['username'], reader['password'], reader['createtime'], reader['lastlogin'], reader['exp'], reader['inventory'], reader['position'])
    Locations[player.position].displayplaces(player)