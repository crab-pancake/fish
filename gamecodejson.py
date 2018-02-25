import random
import time
import csv
import json

class Item(object):
    """items"""
    def __init__(self, code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type):
        self.code = code
        self.item_name = item_name
        self.description = description
        self.exp = exp
        self.min_level = min_level
        self.sale_p = sale_p
        self.buy_p = buy_p
        self.h2 = h2
        self.h3 = h3
        self.i_type = i_type
        self.type = 'other'
    def __str__(self):
        return "Item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Item(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Fish(Item):
    def __init__(self, code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type):
        super().__init__(code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type)
        self.type = 'fish'
        self.sell_price = 5
    def __str__(self):
        return "Fish item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Fish(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Bait(Item):
    def __init__(self, code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type):
        super().__init__(code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type)
        self.type = 'bait'
    def __str__(self):
        return "Bait item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Bait(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Material(Item):
    def __init__(self, code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type):
        super().__init__(code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type)
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
with open('allitems_m.csv', 'r') as readfile:
    reader = csv.DictReader(readfile)
    for row in reader:
        if row['i_type'] == 'fish':
            ThisItem = Fish(row['code'], row['item_name'], row['description'], row['exp'], row['min_level'], row['sale_p'], row['buy_p'], row['h2'], row['h3'], row['i_type'])
            ListOfItems[ThisItem.code] = ThisItem
        elif row['i_type'] == 'bait':
            ThisItem = Bait(row['code'], row['item_name'], row['description'], row['exp'], row['min_level'], row['sale_p'], row['buy_p'], row['h2'], row['h3'], row['i_type'])
            ListOfItems[ThisItem.code] = ThisItem
        else:
            ThisItem = Item(row['code'], row['item_name'], row['description'], row['exp'], row['min_level'], row['sale_p'], row['buy_p'], row['h2'], row['h3'], row['i_type'])
        ListOfItems[ThisItem.code] = ThisItem

class Player(object):
    def __init__(self, username, password, createtime, lastlogin, exp, inventory, position):
        self.username = username
        self.password = password
        self.createtime = createtime
        self.lastlogin = lastlogin
        self.exp = exp
        self.inventory = inventory
        self.position = position
        self.hsll = (time.time() - float(lastlogin))/3600
    def updatetime(self):
        self.lastlogin = time.time()
    def save(self):
        stats = {
        "username": self.username, 
        "password": self.password, 
        "create time": self.createtime, 
        "last login": self.lastlogin,
        "exp": self.exp,
        "inventory": self.inventory,
        "position": self.position
        }
        with open(self.username+'_p.json', 'w') as file:
            json.dump(stats, file)
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
                self.shop_display("shop_basic","01")
            elif menu == "4":
                self.help_display()
            elif menu == "5":
                print ("Saving and exiting game.")
                self.save()
                print ("Complete.")
                break
            else:
                self.error_message()
    def suc_fish(self, fish_exp):
        print ("You have",self.inventory['00000'],"fishing juice remaining.")
        self.exp['fishing'] += fish_exp
        self.save()
    def fish_away(self):   #update so that catching nothing is determined first, then chance of each fish
        self.locations = []
        # FishingSpot = input("Where do you want to fish?\n> ")
        with open('droppers_l.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader: 
                if self.exp['fishing'] > int(row['min_level']):
                    place = Location(row['name'], row['description'], row['min_level'])
                    self.locations.append(place)
        for number, place in enumerate(self.locations, 1):
            print('%s. %s' %(number, place))

        loottable = 'table' #loottable will be changed to the player's specific level loottable
        with open(loottable+'_t.csv', 'r') as table:
            self.table = dict(csv.reader(table))
            while True:
                fish = input("Would you like to fish? Press Y for yes, N for no.\n>> ").strip().lower()
                if fish == "y":
                    if self.inventory['00000'] >0:
                        self.inventory['00000'] -= 1
                        rng = random.randint(1,100)
                        catch = False
                        for key in self.table:
                            if rng >= int(self.table[key]):
                                self.inventory[key] =  int(self.inventory[key]) +1
                                print("You caught a [",ListOfItems[key].item_name,'] .')
                                print("You have",self.inventory[key],ListOfItems[key].item_name+'.')
                                self.suc_fish(int(ListOfItems[key].exp))
                                catch = True
                                break
                        if catch == False:
                            print("You didn't catch anything.")
                            self.suc_fish(0)
                    else:
                        print ("You have no units of fishing juice left. Try waiting at least another hour.")
                elif fish == "n":
                    break
                else:
                    print ("Invalid response, try again.\n")
    def disp_gold(self):
        print("You now have %s %s." % (self.inventory['00001'],ListOfItems['00001'].description))
    def shop_display(self,shop_b_type,shop_s_type):
        while True:
            shop = input("\nWelcome to the General Store. Here you can sell your hard earned fish and purchase new equipment to upgrade your fishing capabilities. \nPress 's' to sell items and 'b' to purchase items.")
            if shop == 's':
                self.shop_sell(shop_s_type)
            elif shop == 'b':
                self.shop_buy(shop_b_type)
            elif shop == 'x':
                break
            else:
                self.error_message()
    def shop_buy(self, shop_b_type):#shop_b_type - this refers to the CSV file of the purchasing shop. This CSV should have a dictionary of items codes (e.g. 02001) as keys, as well as blank filler values
        with open(shop_b_type+'_s.csv', 'r') as shop:
            self.shop = dict(csv.reader(shop))
            print("\nAlright, here's what's available for purchase.\n")
            for key in self.shop:
                print("%s - Cost: %s" % (ListOfItems[key].description, ListOfItems[key].buy_p))
            self.disp_gold()
            while True: 
                purchase = input("\nType in the EXACT name of the item you wish to purchase. Or press x to return.\n").lower()
                if purchase == 'x':
                    break
                itemfound = False
                for key in self.inventory:
                    if ListOfItems[key].description.lower() == purchase:
                        itemfound = True
                        buyitem = ListOfItems[key]
                        while True:
                            try:
                                purchase_q = input("How many [%s] would you like to purchase? Purchase price: [%s]" % (buyitem.description, buyitem.buy_p))
                                if int(purchase_q) > int(round(self.inventory['00001']/int(buyitem.buy_p))) or int(purchase_q) < 0: #0<q<num
                                    self.error_message()
                                elif purchase_q == 'x':
                                    break
                                else:
                                    self.inventory[key] += int(purchase_q)
                                    self.inventory['00001'] -= int(purchase_q)*int(buyitem.buy_p)
                                    print("You now have %s %s." % (self.inventory[key],buyitem.description))
                                    self.disp_gold()
                                    self.save()
                                    break
                            except ValueError:
                                self.error_message()
                if itemfound == False:
                    self.error_message()
                
    def shop_sell(self,shop_s_code):#shop_s_code - this can be used to define a type of shop. e.g. '01' - corresponds to a fishing shop, where you can sell all your fish.
        while True:
            print("\nYou have the following fish available for sale:\n")
            for key in self.inventory:
                if key[:2] == shop_s_code:
                    sell_fish = ("%s :%s    Sale price:%s" % (ListOfItems[key].description, self.inventory[key], ListOfItems[key].sale_p))
                    print(sell_fish)
            self.disp_gold()
            sale = input("Type in the EXACT name of the item you wish to sell. Or press x to return.").lower()
            if sale == 'x':
                break
            for key in self.inventory:
                if ListOfItems[key].description.lower() == sale:
                    while True:
                        try:                    
                            sale_q = int(input("How many [%s] would like you to sell? Maximum number to sell: [%s] Sale price: [%s]\n" % (ListOfItems[key].description, self.inventory[key], ListOfItems[key].sale_p)))
                            if sale_q > self.inventory[key] or 0 > sale_q:
                                self.error_message()
                            else:
                                self.inventory[key] -= sale_q
                                self.inventory['00001'] += sale_q*int(ListOfItems[key].sale_p)
                                print("You now have %s %s." % (self.inventory[key],ListOfItems[key].description))
                                self.disp_gold()
                                self.save()
                                break
                        except ValueError:
                            self.error_message()

    def help_display(self):
        print("\nHELP\n"
            "\n----------------------------\n"
            "\nHistory:\nJerry and Dayu thought of this game as they were walking with Evan and Mummy, along Lake Nordenskjoeld, W-Trek, Patagonia, Chile in late December 2017. The inspiration came from many hours of idle chat, but at least it encouraged them to do somethiing productive!\n"
            "\nAim:\nThis is a time based game, where you as the player character gather 'fishing juice' to catch fish, upgrade your setup and further your fishing capabilities.\n"
            "\nInitial setup:\nYou'll begin with 10 fishing juice and no fish. Under the 'Menu' option, choose 'Fish!' to use up your fishing juice and catch fish.\n"
            "Each time you'll have a go at fishing and deplete your fishing juice by one. You'll gather more fishing juice by logging off (1 per hour is the base rate) and relogging on.\n"
            "\nBuying and selling:\n Enter the corresponding number 'Visit shop' in order to buy and sell your fish to gain gold. Use your gold to upgrade your fishing set up. For example, the cheapest upgrade will is the 'Reinforced net', which will increase your fishing juice gathering rate by 10%.\n"
            "\nFinal words:\n Good luck! We'll be slowly adding in extra features, but be patient as we are new :3")
    def error_message(self):
        print ("Error: That is invalid. Try again.")
    def inv_display(self): 
        print("YOUR INVENTORY:\n-------------------------")
        for key in self.inventory:
            print('%s: %s' % (ListOfItems[key].description, self.inventory[key]))



# indent=2, sort_keys=True
# with open('things.json', 'r') as file:
#     reader = json.load(file) # This returns a dictionary with all the information in it. 
#     player = Player(reader['username'], reader['password'], reader['create time'], reader['last login'], reader['exp'], reader['inventory'], reader['position'])

def rungame(uname):
    with open(uname+'_p.json', 'r') as file:
        reader = json.load(file)
        player = Player(reader['username'], reader['password'], reader['create time'], reader['last login'], reader['exp'], reader['inventory'], reader['position'])

        if player.lastlogin == 0: #If this is the first access of the game, then ptimeraw == 0
            print('running first mode') #for debug purposes
            player.updatetime()
            player.inventory = dict.fromkeys(ListOfItems, 0)
            player.save()
            player.inventory['00000'] = 10  #when a new account is created, 10 fishing juice is given
            print ("Welcome to the game! This is your first login. \n"
                   "Account creation time: %s"% (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(player.createtime))))
            player.display_menu()
            player.save()

        elif player.lastlogin - player.createtime > 0: 
            print('running second mode') #for debug purposes
            player.updatetime()
            player.save()
            player.inventory['00000'] += int(player.hsll)
            print ("___________________\n"
                   "Welcome back to the game!\n"
                   "Account creation time: %s\n"
                   "Time since last login: %s hrs, %s mins\n\n"
                   "You've acquired [ %s ] unit(s) of fishing juice since the last login. \n"   
                   "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n" 
                   %(player.createtime, int(player.hsll), int((player.hsll-int(player.hsll))*60), int(player.hsll)))
            player.display_menu()
            player.save()

        elif player.lastlogin - player.createtime < 0:
            print("Error happened.")

if __name__ == "__main__":
    with open('test_acct_p.json', 'w', ) as file:
        stats = {"username": "test_acct", "password": "","create time": time.time(),"last login": 0,
            "exp": {"fishing": 0},"inventory": {"00000": 10},"position": "here"}
        json.dump(stats, file)
    rungame('test_acct')

print("Thanks for playing! Come back soon.")