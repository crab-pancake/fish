import csv
import json
import universals as univ
import random
import ingameMenu



class Location(object):
    def __init__(self, code, name, description, travel):
        self.code = code
        self.name = name
        self.description = description
        self.places = {0:('Leave', self.travel), 1:('Do a thing', 'funcname')}
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

    def displayplaces(self, player):
        self.player = player
        print("You are currently at %s." % (self.name))
        while True:
            print("Which place do you want to go into?")
            for num, place in sorted(self.places.items())[1:]:
                print(num, self.places[num][0])
            print(0, self.places[0][0])
            choice=univ.IntChoice(len(self.places),['x','m'],[0])
            if choice == 'x' or choice == 0:
                return self.travel()
            elif choice == 'm':
                ingameMenu.menu(self.player)
            else: 
                print("test thing has been selected.")
                self.places[choice][1].takeaction(player)

    def travel(self):
        print("You are leaving %s."%(self.name))
        self.traveller = {0:'Return'}
        print('Type the number of the town you want to travel to.')
        for location in sorted(self.destinations):
            i=1
            self.traveller[i] = Locations[location].name
        for num, loc in sorted(self.traveller.items())[1:]:
            print(num, self.traveller[num])
        print(0,self.traveller[0])
        while True:
            choice=univ.IntChoice(len(self.traveller), ['x','m'], [0])
            if choice == 0 or choice == 'x':
                print('Returning to old place... ')
                return self.code
            elif choice == 'm':
                ingameMenu.menu(self.player)
            else:
                newpos = sorted(self.destinations)[choice-1]
                print('You have moved to %s.'%(Locations[newpos].name))
                print(Locations[newpos].description) # just testing
                return newpos

class Place(object):
    def __init__(self, code, name, description,Type):
        self.code = code
        self.name = name
        self.description = description
        self.actions = {1:('Do something', self.dosomething), 2:('Talk to the owner', self.talk), 0:('Leave', self.leave)}
    def takeaction(self,player):
        self.player=player
        print("What do you want to do?")
        while True:
            for key, val in sorted(self.actions.items())[1:]:
                print(key, val[0])
            print(0, self.actions[0][0])
            choice=univ.IntChoice(len(self.actions), ['x','m'],[0])
            if choice == 'x' or choice == 0:
                self.leave()
                break
            elif choice == 'm':
                ingameMenu.menu(player)
            else:
                self.actions[choice][1]()
    def dosomething(self):
        print('Something has been done.')
    def talk(self):
        print('Talking to owner...')
    def leave(self):
        print("Leaving.")

class Shop(Place):
    """Class for shops selling different things."""
    def __init__(self, code, name,description,Type, IntroLine, ExitLine):
        super().__init__(code,name,description,Type)
        self.intro = IntroLine
        self.exit = ExitLine
        self.actions[3] = ('Shop', self.shopfront)
        # with open(code+'_s.csv', 'r') as file:
            # pass
    def shopfront(self):
        print(self.intro)
        print("""What would you like to do?
1. Sell
2. Buy
3. Exit""")
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
    def StartFishing(self):
        with open(self.loottable, 'r') as file:
            reader = dict(csv.reader(file))
            while True:
                fish = input("Would you like to fish? Press Y for yes, N for no.\n>> ").strip().lower()
                if fish == "y":
                    if gamecode.player.inventory['i00000'] >0:
                        gamecode.player.inventory['i00000'] -= 1
                        rng = random.randint(1,100)
                        catch = False
                        for key in reader:
                            if rng >= int(reader[key]):
                                player.inventory[key]+=1
                                print('You caught a [',univ.ListOfItems[key].item_name,'] .')
                                print("You have",player.inventory[key],univ.ListOfItems[key].item_name+'.')
                                # self.suc_fish(univ.ListOfItems[key].exp)
                                print("You got %s exp" % (univ.ListOfItems[key].exp))
                                catch = True
                                break
                        if catch == False:
                            print("You didn't catch anything.")
                            # self.suc_fish(0)
                    else: print ("You have no units of fishing juice left. Try waiting at least another hour.")
                elif fish == "n": 
                    self.takeaction()
                    break
                else:  univ.error(2)
    def suc_fish(self, fish_exp):
        print ("You have",self.inventory['i00000'],"fishing juice remaining.")
        self.exp['fishing'] += fish_exp
        self.save()

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