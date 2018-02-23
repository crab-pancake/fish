import random
import time
import csv

print('gamecode has started')
class User_s(object):
    """user stats file for times and such."""
    def __init__(self, f_time_raw, p_time_raw, pw, uname, exp):
        self.f_time_raw = f_time_raw
        self.p_time_raw = p_time_raw
        self.pw = pw
        self.delta = float(p_time_raw) - float(f_time_raw)
        self.uname = uname
        self.f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(f_time_raw)))
        self.p_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(p_time_raw)))
        self.hsll = (time.time() - float(p_time_raw))/3600
        self.exp = exp
    def update_time(self):
        self.p_time_raw = time.time()
    def save(self):
        stats = {"Create Time":self.f_time_raw, "Last Login": self.p_time_raw, "Password":self.pw, "exp": self.exp}
        with open(self.uname+'_i.csv', 'w', newline='') as savefile:
            writer = csv.writer(savefile, dialect='excel')
            for key, value in stats.items():
                writer.writerow([key, value])

class Item(object):
    """items"""
    def __init__(self, code, item_name, description, exp, min_level):
        self.code = code
        self.item_name = item_name
        self.description = description
        self.exp = exp
        self.min_level = min_level
        self.type = 'other'
    def __str__(self):
        return "Item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Item(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Fish(Item):
    def __init__(self, code, item_name, description, exp, min_level):
        super().__init__(code, item_name, description, exp, min_level)
        self.type = 'fish'
        self.sell_price = 5
    def __str__(self):
        return "Fish item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Fish(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Bait(Item):
    def __init__(self, code, item_name, description, exp, min_level):
        super().__init__(code, item_name, description, exp, min_level)
        self.type = 'bait'
    def __str__(self):
        return "Bait item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Bait(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Material(Item):
    def __init__(self, code, item_name, description, exp, min_level):
        super().__init__(code, item_name, description, exp, min_level)
        self.type = 'material'
    def __str__(self):
        return "Material item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Material(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Location(object):
    """Fishing Locations class"""
    def __init__(self, name, description, min_level):
        self.name = name
        self.description = description
        self.min_level = min_level
    def __str__(self):
        return "Fishing location %s, minimum level %s" % (self.name, self.min_level)
    def __repr__(self):
        return "Location(self, %r, %r, %r, %r)" % (self.name, self.description, self.min_level)

ListOfItems = {}
print('listofitems has been made')
with open('allitems.csv', 'r') as readfile:
    reader = csv.DictReader(readfile)
    for row in reader:
        if row['i_type'] == 'fish':
            ThisItem = Fish(row['code'], row['item_name'], row['description'], row['exp'], row['min_level'])
            ListOfItems[ThisItem.code] = ThisItem
        elif row['i_type'] == 'bait':
            ThisItem = Bait(row['code'], row['item_name'], row['description'], row['exp'], row['min_level'])
            ListOfItems[ThisItem.code] = ThisItem
        else:
            ThisItem = Item(row['code'], row['item_name'], row['description'], row['exp'], row['min_level'])
        ListOfItems[ThisItem.code] = ThisItem

class User_g(object):
    """Docstring"""
    def __init__(self, uname):
        self.uname = uname
        self.inv = {}
        self.allitems = ListOfItems
        for key in self.allitems:
            self.inv[key] = 0      #creates a dictionary called inv and creates keys for all the entries from allitems, sets all quantities to 0
    def load(self):   #done
        with open(self.uname+'_g_info.csv', 'r') as loadfile:
            loader = dict(csv.reader(loadfile))
            for key in loader:
                self.inv[key] = int(loader[key])
    def save(self):   #done
        with open(self.uname+'_g_info.csv', 'w', newline='') as savefile:
            writer = csv.writer(savefile, dialect = 'excel')
            for key, value in self.inv.items():
                # if value or key == ['00000']: # if value!=0
                    writer.writerow([key, value])
    def fish_away(self):   #update so that catching nothing is determined first, then chance of each fish
        self.locations = []
        # FishingSpot = input("Where do you want to fish?\n> ")
        with open('droppers.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader: 
                if int(player_s.exp) > int(row['min_level']):
                    place = Location(row['name'], row['description'], row['min_level'])
                    self.locations.append(place)
        for place in self.locations:
            print(place)

        loottable = 'table' #loottable will be changed to the player's specific level loottable
        with open(loottable+'.csv', 'r') as table:
            self.table = dict(csv.reader(table))
            while True:
                fish = input("Would you like to fish? Press Y for yes, N for no.\n>> ").strip().lower()
                if fish == "y":
                    if self.inv['00000'] >0:
                        self.inv['00000'] -= 1
                        rng = random.randint(1,100)
                        catch = False
                        for key in self.table:
                            if rng >= int(self.table[key]):
                                self.inv[key] =  int(self.inv[key]) +1
                                print("You caught a [",self.allitems[key].item_name,'] .')
                                print("You have",self.inv[key],self.allitems[key].item_name+'.')
                                self.suc_fish(self.allitems[key].exp)
                                catch = True
                                break
                        if catch == False:
                            print("You didn't catch anything.")
                            self.suc_fish('0')
                    else:
                        print ("You have no units of fishing juice left. Try waiting at least another hour.")
                elif fish == "n":
                    break
                else:
                    print ("Invalid response, try again.\n")
    def suc_fish(self, fish):
        print ("You have",self.inv['00000'],"fishing juice remaining.")
        player_s.exp = int(player_s.exp) + int(fish)
        self.save()

    def shop_display(self):
        print("Coles")
    def help_display(self):
        print("\nHELP\n"
            "\n----------------------------\n"
            "\nHistory:\nJerry and Dayu thought of this game as they were walking with Evan and Mummy, along Lake Nordenskjoeld, W-Trek, Patagonia, Chile in late December 2017. The inspiration came from many hours of idle chat, but at least it encouraged them to do somethiing productive!\n"
            "\nAim:\nThis is a time based game, where you as the player character gather 'fishing juice' to catch fish, upgrade your setup and further your fishing capabilities.\n"
            "\nInitial setup:\nYou'll begin with 10 fishing juice and no fish. Under the 'Menu' option, choose 'Fish!' to use up your fishing juice and catch fish.\n"
            "Each time you'll have a go at fishing and deplete your fishing juice by one. You'll gather more fishing juice by logging off (1 per hour is the base rate) and relogging on.\n"
            "\nBuying and selling:\n Enter the corresponding number 'Visit shop' in order to buy and sell your fish to gain gold. Use your gold to upgrade your fishing set up. For example, the cheapest upgrade will is the 'Reinforced net', which will increase your fishing juice gathering rate by 10%.\n"
            "\nFinal words:\n Good luck! We'll be slowly adding in extra features, but be patient as we are new :3")
    def display_menu(self):
    	while True:
            menu = input("\nMENU\n"
                    "----------------------------\n"
                    "1. Display inventory\n"
                    "2. Fish!\n"
                    "3. Visit shop (sell and buy items)\n"
                    "4. Help\n"
                    "5. Exit game\n> ")
            if menu =="1":
                self.inv_display()
            elif menu =="2":
                self.fish_away()
            elif menu == "3":
                self.shop_display()
            elif menu == "4":
                self.help_display()
            elif menu == "5":
                print ("Saving and exiting game.")
                self.save()
                print ("Complete.")
                break
            else:
                self.error_message()
    def error_message(self):
        print ("Try again.")
    def inv_display(self): 
        print("YOUR INVENTORY:\n-------------------------")
        for key in self.inv:
            print('%s: %s' % (self.allitems[key].item_name, self.inv[key]))

def rungame(uname):
    with open(uname+'_i.csv', 'r') as file:
        global player_s
        playerfile = dict(csv.reader(file))
        player_s = User_s(playerfile["Create Time"], playerfile["Last Login"], playerfile["Password"], uname, playerfile["exp"])

        if player_s.p_time_raw == '0': #If this is the first access of the game, then ptimeraw == 0
            print('running first mode') #for debug purposes
            player_s.update_time()
            player_s.save()
            player_g = User_g(uname)
            player_g.inv['00000'] = 10  #when a new account is created, 10 fishing juice is given
            print ("Welcome to the game! This is your first login. \n"
                   "Account creation time: %s"%(player_s.f_time))
            player_g.display_menu()
            player_s.save()

        elif player_s.delta > 0: 
            print('running second mode') #for debug purposes
            player_g = User_g(uname)
            player_s.update_time()
            player_s.save()
            player_g.load()
            player_g.inv['00000']=int(player_g.inv['00000'])+int(player_s.hsll)
            print ("___________________\n"
                   "Welcome back to the game!\n"
                   "Account creation time: %s\n"
                   "Time since last login: %s hrs, %s mins\n\n"
                   "You've acquired [ %s ] unit(s) of fishing juice since the last login. \n"   
                   "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n" 
                   %(player_s.f_time, int(player_s.hsll), int((player_s.hsll-int(player_s.hsll))*60), int(player_s.hsll)))
            player_g.display_menu()
            player_s.save()

        elif (player_s.delta < 0):
            print("Error happened.")
            player_s.close()

if __name__ == "__main__":
    pass

print("Thanks for playing! Come back soon.")