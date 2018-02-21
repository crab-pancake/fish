import random
import time
import csv

print('gamecode has started')
# global obj
# obj='potato'

# class NewItem(object):
#     """items"""
#     def __init__(self, code, name, description, exp, min_level):
#         self.code = code
#         self.name = name
#         self.description = description
#         self.exp = exp
#         self.min_level = min_level
#         self.type = obj
#         print(obj)
#     def __str__(self):
#         return 'Item class object'
#     def printname(self):
#         print (self.name)

# class NewFish(NewItem):
#     def __init__(self, code, name, description, exp, min_level):
#         super().__init__(code, name, description, exp, min_level)
#         self.type = 'fish'

# items = {}
# print(obj)
# with open('test.csv', 'r') as file:
#     reader = csv.DictReader(file)
#     print(obj*2)
#     for row in reader:
#         if row['code'] == '002':
#             item = NewFish(row['code'], row['name'], row['description'], row['exp'], row['min_level'])
#             print('this happens')
#         else:
#             item = NewItem(row['code'], row['name'], row['description'], row['exp'], row['min_level'])
#             print('this also happens')
#         print(obj)
#         items[item.code] = item

# items['002'].printname()
# print(items['001'].type)
# print(items['003'].type)
# print(items['002'].type)

# print(items['003'])

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
        return "Item(self, %r, %r, %r, %r, %r)" % (self.code, self.name, self.description, self.exp, self.min_level)

class Fish(Item):
    def __init__(self, code, name, description, exp, min_level):
        super().__init__(code, name, description, exp, min_level)
        self.type = 'fish'
        self.sell_price = 5
    def __str__(self):
        return "Fish item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Fish(self, %r, %r, %r, %r, %r)" % (self.code, self.name, self.description, self.exp, self.min_level)

class Bait(Item):
    def __init__(self, code, name, description, exp, min_level):
        super().__init__(code, name, description, exp, min_level)
        self.type = 'bait'
    def __str__(self):
        return "Bait item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Bait(self, %r, %r, %r, %r, %r)" % (self.code, self.name, self.description, self.exp, self.min_level)

class Material(Item):
    def __init__(self, code, name, description, exp, min_level):
        super().__init__(code, name, description, exp, min_level)
        self.type = 'material'
    def __str__(self):
        return "Material item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Material(self, %r, %r, %r, %r, %r)" % (self.code, self.name, self.description, self.exp, self.min_level)

global ListOfItems
ListOfItems = {}
print('listofitems has been made')
with open('test.csv', 'r') as readfile:
    reader = csv.DictReader(readfile)
    for row in reader:
        # if row['i_type'] == 'fish':
        #     ThisItem = Fish(row['code'], row['name'], row['description'], row['exp'], row['min_level'])
        #     ListOfItems[ThisItem.code] = ThisItem
        # elif row['i_type'] == 'bait':
        #     ThisItem = Bait(row['code'], row['name'], row['description'], row['exp'], row['min_level'])
        #     ListOfItems[ThisItem.code] = ThisItem
        # else:
        ThisItem = Item(row['code'], row['name'], row['description'], row['exp'], row['min_level'])
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
                    if self.inv['000'] >0:
                        self.inv['000'] -= 1
                        rng = random.randint(1,100)
                        catch = False
                        for key in self.table:
                            if rng >= int(self.table[key]):
                                self.inv[key] =  int(self.inv[key]) +1
                                print("You caught a [",self.allitems[key].name,'] .')
                                print("You have",self.inv[key],self.allitems[key].name+'.')
                                self.suc_fish(key)
                                catch = True
                                break
                        if catch == False:
                            print("You didn't catch anything.")
                            self.suc_fish('000')
                    else:
                        print ("You have no units of fishing juice left. Try waiting at least another hour.")
                elif fish == "n":
                    break
                else:
                    print ("Invalid response, try again.\n")
    def suc_fish(self, fish):
        print ("You have",self.inv['000'],"fishing juice remaining.")
        player_s.exp = int(player_s.exp)
        player_s.exp += int(self.allitems[fish].exp)
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
            print('%s: %s' % (self.allitems[key].name, self.inv[key]))

global player_s
player_s = User_s(playerfile["Create Time"], playerfile["Last Login"], playerfile["Password"], uname, playerfile["exp"])

if player_s.p_time_raw == '0': #If this is the first access of the game, then ptimeraw == 0
    print('running first mode') #for debug purposes
    player_s.update_time()
    player_s.save()
    player_g = User_g(uname)
    player_g.inv['000'] = 10  #when a new account is created, 10 fishing juice is given
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
    player_g.inv['000']=int(player_g.inv['000'])+int(player_s.hsll)
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