import random
import time
import csv

class User_s(object):
    """user stats file for times and such."""
    def __init__(self, f_time_raw, p_time_raw, pw, uname):
        self.f_time_raw = f_time_raw
        self.p_time_raw = p_time_raw
        self.pw = pw
        self.delta = float(p_time_raw) - float(f_time_raw)
        self.uname = uname
        self.f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(f_time_raw)))
        self.p_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(p_time_raw)))
        self.hsll = (time.time() - float(p_time_raw))/3600
    def update_time(self):
        self.p_time_raw = time.time()
    def save(self):
        stats = {"Create Time":self.f_time_raw, "Last Login": self.p_time_raw, "Password":self.pw}
        with open(self.uname+'_i.csv', 'w', newline='') as savefile:
            writer = csv.writer(savefile, dialect='excel')
            for key, value in stats.items():
                writer.writerow([key, value])

class Item(object):
    """items"""
    def __init__(self, code, name, description, exp, min_level):
        self.code = code
        self.name = name
        self.description = description
        self.exp = exp
        self.min_level = min_level
        self.type = 'other'
    def __str__(self):
        return "Item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Item(self, %s, %s, %s, %s, %s)" % (self.code, self.name, self.description, self.exp, self.min_level)
class Fish(Item):
    def __init__(self, code, name, description, exp, min_level):
        super().__init__(code, name, description, exp, min_level)
        self.type = 'fish'
        self.sell_price = 5
    def __str__(self):
        return "Fish with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Fish(self, %s, %s, %s, %s, %s)" % (self.code, self.name, self.description, self.exp, self.min_level)
class Bait(Item):
    def __init__(self,a):
        super().__init__(code, name, description, exp, min_level)
        self.type = 'bait'
    def __str__(self):
        return "Bait with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Bait(self, %s, %s, %s, %s, %s)" % (self.code, self.name, self.description, self.exp, self.min_level)
class Material(Item):
    def __init__(self,a):
        super().__init__(code, name, description, exp, min_level)
        self.type = 'material'

items = {}

class User_g(object):
    """ A User's account. Defines the amount of fishing juice and starting items."""
    def __init__(self, uname):
        self.uname = uname
        self.inv = {}
        self.allitems = 0
        with open('allitems.csv', 'r') as allitems:   #allitems is stored as itemabbrev: item display name. Eventually change this to a dictreader object
            self.allitems = dict(csv.reader(allitems))
        for key in self.allitems:
            self.inv[key] = 0      #creates a dictionary called inv and creates keys for all the entries from allitems, sets all quantities to 0
    def load(self):   #done
        with open(self.uname+'_g_info.csv', 'r') as loadfile:
            loader = dict(csv.reader(loadfile))
            for key in loader:
                self.inv[key] = loader[key]
    def save(self):   #done
        with open(self.uname+'_g_info.csv', 'w', newline='') as savefile:
            writer = csv.writer(savefile, dialect = 'excel')
            for key, value in self.inv.items():
                writer.writerow([key, value])
    def fish_away(self):   #update so that catching nothing is determined first, then chance of each fish
        with open('table.csv', 'r') as table: #table.csv will be changed to the player's specific level loottable
            self.table = dict(csv.reader(table))
            while True:
                fish = input("Would you like to fish? Press Y for yes, N for no.\n>> ").strip().lower()
                if fish == "y":
                    if self.inv['f_j'] >0:
                        self.inv['f_j'] -= 1
                        rng = random.randint(1,100)
                        catch = False
                        for key in self.table:
                            if rng >= int(self.table[key]):
                                self.inv[key] =  int(self.inv[key]) +1
                                print("You caught a",key+'.')
                                print("You have",self.inv[key],key+'.') #how can I add a description? May have to move away from csv files or dictionaries
                                self.suc_fish()
                                catch = True
                                break
                        if catch == False:
                            print("You didn't catch anything.")
                            self.suc_fish()
                    else:
                        print ("You have no units of fishing juice left. Try waiting at least another hour.")
                elif fish == "n":
                    break
                else:
                    print ("Invalid response, try again.\n")
    def suc_fish(self):
        print ("You have",self.inv['f_j'],"fishing juice remaining.")
        self.save()

    def shop_display(self):
        print("Coles")
    def help_display(self):
        print("help me pls")
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
            print('%s: %s' % (self.allitems[key], self.inv[key]))

player_s = User_s(stats["Create Time"], stats["Last Login"], stats["Password"], uname)

if player_s.p_time_raw == '0': #If this is the first access of the game, then ptimeraw == 0
    print('running first mode') #for debug purposes
    player_s.update_time()
    player_s.save()
    player_g = User_g(uname)
    player_g.inv['f_j'] = 10  #when a new account is created, 10 fishing juice is given
    print ("Welcome to the game! This is your first login. \n"
           "Account creation time: %s"%(player_s.f_time))
    player_g.display_menu()

elif player_s.delta > 0: 
    print('running second mode') #for debug purposes
    player_g = User_g(uname)
    player_s.update_time()
    player_s.save()
    player_g.load()
    player_g.inv['f_j']=int(player_g.inv['f_j'])+int(player_s.hsll)
    print ("___________________\n"
           "Welcome back to the game!\n"
           "Account creation time: %s\n"
           "Time since last login: %s hrs, %s mins\n\n"
           "You've acquired [ %s ] unit(s) of fishing juice since the last login. \n"   
           "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n" 
           %(player_s.f_time, int(player_s.hsll), int((player_s.hsll-int(player_s.hsll))*60), int(player_s.hsll)))
    player_g.display_menu()

elif (player_s.delta < 0):
    print("Error happened.")