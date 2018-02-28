import random
import time
import csv
import json

import universals as univ

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
    def __init__(self, code, name, description, min_level):
        self.code = code
        self.name = name
        self.description = description
        self.min_level = min_level
    def __str__(self):
        return "Fishing location %s, minimum level %s" % (self.name, self.min_level)
    def __repr__(self):
        return "Location(self, %r, %r, %r, %r, %r)" % (self.code, self.name, self.description, self.min_level)

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
        "createtime": self.createtime,
        "lastlogin": self.lastlogin,
        "exp": self.exp,
        "inventory": self.inventory,
        "position": self.position
        }
        with open('./PlayerAccts/'+self.username+'_p.json', 'w') as file:
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
                self.shop_display("shop_basic","i01")
            elif menu == "4":
                self.help_display()
            elif menu == "5":
                print ("Saving and exiting game.")
                self.save()
                print ("Complete.")
                break
            else:
                self.error_message(0)
    def suc_fish(self, fish_exp):
        print ("You have",self.inventory['i00000'],"fishing juice remaining.")
        self.exp['fishing'] += fish_exp
        self.save()
    def fish_away(self):   #update so that catching nothing is determined first, then chance of each fish
        self.locations = []
        with open('droppers_l.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader: 
                if self.exp['fishing'] >= int(row['min_level']):
                    place = Location(row['code'], row['name'], row['description'], row['min_level'])
                    self.locations.append(place)
        for number, place in enumerate(self.locations, 1):
            print('%s. %s' %(number, place))
        while True:
            try:
                FishingSpot = int(input("Where do you want to fish? Type a number from 1 to %s \n> " % (len(self.locations))))
                if 0<FishingSpot<=len(self.locations):
                    break
                else:
                    self.error_message(0)
            except ValueError:
                self.error_message(0)
        with open('./tables/'+self.locations[FishingSpot-1].code+'_t.csv', 'r') as table:
            self.table = dict(csv.reader(table))
            while True:
                fish = input("Would you like to fish? Press Y for yes, N for no.\n>> ").strip().lower()
                if fish == "y":
                    if self.inventory['i00000'] >0:
                        self.inventory['i00000'] -= 1
                        rng = random.randint(1,100)
                        catch = False
                        for key in self.table:
                            if rng >= int(self.table[key]):
                                self.inventory[key] =  self.inventory[key] +1
                                print("You caught a [",univ.ListOfItems[key].item_name,'] .')
                                print("You have",self.inventory[key],univ.ListOfItems[key].item_name+'.')
                                self.suc_fish(univ.ListOfItems[key].exp)
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
    def disp_currency(self, currency):
        print("You now have %s %s." % (self.inventory[currency],univ.ListOfItems[currency].description))
    def shop_display(self,shop_b_type,shop_s_type):
        while True:
            shop = input("""Welcome to the General Store.
Here you can sell your hard earned fish and purchase new equipment to upgrade your fishing capabilities.
Press 's' to sell items and 'b' to purchase items. Or press 'x' to leave. 
>> """).strip().lower()
            if shop == 's':
                self.shop_sell(shop_s_type)
            elif shop == 'b':
                self.shop_buy(shop_b_type)
            elif shop == 'x':
                break
            else:
                self.error_message(0)
    def shop_buy(self, shop_b_type):#shop_b_type refers to the CSV file of the purchasing shop. This CSV should have a dictionary of items codes (e.g. 02001) as keys, as well as blank filler values
        with open(shop_b_type+'_s.csv', 'r') as shop:
            self.shop = dict(csv.reader(shop))
            print("\nAlright, here's what's available for purchase.\n")
            for key in self.shop:
                print("%s - Cost: %s" % (univ.ListOfItems[key].description, univ.ListOfItems[key].buy_p))
            self.disp_currency('i00001')
            while True: 
                purchase = input("\nType in the EXACT name of the item you wish to purchase. Or press x to return.\n>> ").lower()
                if purchase == 'x':
                    break
                itemfound = False
                for key in self.inventory:
                    if univ.ListOfItems[key].description.lower() == purchase:
                        itemfound = True
                        buyitem = univ.ListOfItems[key]
                        while True:
                            purchase_q = input("How many [%s] would you like to purchase? Purchase price: [%s]\n>> " % (buyitem.description, buyitem.buy_p))
                            if purchase_q == 'x':
                                break
                            try:
                                quantity = int(purchase_q)
                                if 0 < int(self.inventory['i00001']) < quantity*univ.ListOfItems[key].buy_p:
                                    self.error_message(0)
                                else:
                                    self.inventory[key] += quantity
                                    self.inventory['i00001'] -= quantity*univ.ListOfItems[key].buy_p
                                    print("You now have %s %s." % (self.inventory[key],univ.ListOfItems[key].description))
                                    self.disp_currency('i00001')
                                    self.save()
                                    break
                            except ValueError:
                                self.error_message(0)
                if itemfound == False:
                    self.error_message(0)
                
    def shop_sell(self,shop_s_code):#shop_s_code - this can be used to define a type of shop. e.g. '01' - corresponds to a fishing shop, where you can sell all your fish.
        while True:
            print("\nYou have the following fish available for sale:\n")
            for key in self.inventory:
                if key[:3] == shop_s_code:
                    sell_fish = ("%s :%s    Sale price:%s" % (univ.ListOfItems[key].description, self.inventory[key], univ.ListOfItems[key].sale_p))
                    print(sell_fish)
            self.disp_currency('i00001')

            sale = input("Type in the EXACT name of the item you wish to sell. Or type x to return.\n>> ").lower()
            if sale == 'x':
                break
            for key in self.inventory:
                if univ.ListOfItems[key].description.lower() == sale:
                    while True:
                        try:                    
                            sale_q = int(input("How many [%s] would like you to sell? Maximum number to sell: [%s] Sale price: [%s]\n>> " 
                                % (univ.ListOfItems[key].description, self.inventory[key], univ.ListOfItems[key].sale_p)))
                            if sale_q > self.inventory[key] or 0 > sale_q:
                                self.error_message(0)
                            else:
                                self.inventory[key] -= sale_q
                                self.inventory['i00001'] += sale_q*univ.ListOfItems[key].sale_p
                                print("You now have %s %s." % (self.inventory[key],univ.ListOfItems[key].description))
                                self.disp_currency('i00001')
                                self.save()
                                break
                        except ValueError:
                            self.error_message(0)

    def help_display(self):
        print("""HELP
----------------------------
History:
Jerry and Dayu thought of this game as they were walking with Evan and Mummy, along Lake Nordenskjoeld, W-Trek, Patagonia, Chile in late December 2017. 
The inspiration came from many hours of idle chat, but at least it encouraged them to do somethiing productive!

Aim:
This is a time based game, where you as the player character gather 'fishing juice' to catch fish, upgrade your setup and further your fishing capabilities.

Initial setup:
You'll begin with 10 fishing juice and no fish. Under the 'Menu' option, choose 'Fish!' to use up your fishing juice and catch fish.
Each time you'll have a go at fishing and deplete your fishing juice by one. 
You'll gather more fishing juice by logging off (1 per hour is the base rate) and relogging on.

Buying and selling:
Enter the corresponding number 'Visit shop' in order to buy and sell your fish to gain gold. Use your gold to upgrade your fishing set up. 
For example, the cheapest upgrade will is the 'Reinforced net', which will increase your fishing juice gathering rate by 10%.

Final words:
Good luck! We'll be slowly adding in extra features, but be patient as we are new :3""")
    def error_message(self, number):
        print ("Error %s: That is invalid. Try again." % (number)) 
    def inv_display(self): 
        print("YOUR INVENTORY:\n-------------------------")
        for key in self.inventory:
            print('%s: %s' % (univ.ListOfItems[key].description, self.inventory[key]))

def rungame(uname):
    with open('./PlayerAccts/'+uname+'_p.json', 'r') as file:
        reader = json.load(file)# This returns a dictionary with all the information in it. 
        player = Player(reader['username'], reader['password'], reader['createtime'], reader['lastlogin'], reader['exp'], reader['inventory'], reader['position'])

        if player.lastlogin == 0: #If this is the first access of the game, then ptimeraw == 0
            print('running first mode') #for debug purposes
            player.updatetime()
            player.inventory = dict.fromkeys(univ.ListOfItems, 0)
            player.save()
            player.inventory['i00000'] = 10  #when account is created, 10 fishing juice is given
            print ("Welcome to the game, %s! This is your first login. \n"
                   "Account creation time: %s"% (player.username, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(player.createtime))))
            player.display_menu()
            player.save()

        elif player.lastlogin - player.createtime > 0: 
            print('running second mode') #for debug purposes
            player.updatetime()
            player.inventory['i00000'] += int(player.hsll)
            player.save()
            print ("___________________\n"
                   "Welcome back to the game, %s!\n"
                   "Account creation time: %s\n"
                   "Time since last login: %s hrs, %s mins\n\n"
                   "You've acquired [ %s ] unit(s) of fishing juice since the last login. \n"   
                   "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n" 
                   %(player.username, player.createtime, int(player.hsll), int((player.hsll%60)*60), int(player.hsll)))
            player.display_menu()

        elif player.lastlogin - player.createtime < 0:
            print("Error happened.")

if __name__ == "__main__":
    with open('./PlayerAccts/test_acct_p.json', 'w', ) as file:
        stats = {"username": "test_acct", "password": "","createtime": time.time(),"lastlogin": 0,
            "exp": {"fishing": 0},"inventory": {},"position": 000}
        json.dump(stats, file)
    rungame('test_acct')

# print("Thanks for playing! Come back soon.") # this prints out before anything else if you run from login module