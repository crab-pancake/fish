import csv
import time
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

ListOfItems = {}
with open('allitems_m.csv', 'r') as readfile:
    reader = csv.DictReader(readfile)
    for row in reader:
        if row['i_type'] == 'fish':
            ThisItem = Fish(row['code'], row['item_name'], row['description'], int(row['exp']), int(row['min_level']), int(row['sale_p']), int(row['buy_p']), row['h2'], row['h3'], row['i_type'])
            ListOfItems[ThisItem.code] = ThisItem
        elif row['i_type'] == 'bait':
            ThisItem = Bait(row['code'], row['item_name'], row['description'], int(row['exp']), int(row['min_level']), int(row['sale_p']), int(row['buy_p']), row['h2'], row['h3'], row['i_type'])
            ListOfItems[ThisItem.code] = ThisItem
        else:
            ThisItem = Item(row['code'], row['item_name'], row['description'], int(row['exp']), int(row['min_level']), int(row['sale_p']), int(row['buy_p']), row['h2'], row['h3'], row['i_type'])
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
                    "4. Help\n"
                    "5. Exit game\n> ")
            if menu =="1":
                self.inv_display()
            elif menu == "4":
                self.help_display()
            elif menu == "5":
                print ("Saving and exiting game.")
                self.save()
                print ("Complete.")
                break
            else: error(0)
    def disp_currency(self, currency):
        print("You now have %s %s." % (self.inventory[currency],univ.ListOfItems[currency].description))
    def help_display(self):
        print("HELP\n")
    def inv_display(self): 
        print("YOUR INVENTORY:\n-------------------------")
        for key in self.inventory:
            print('%s: %s' % (univ.ListOfItems[key].description, self.inventory[key]))

def error(number):
    print ("Error %s: That is invalid. Try again." % (number)) 

yes = ['yes','y','ya','ye','1','True']
no = ['no','na','n','0','False']

def IntChoice(maxvalue,globalexcept, localexcept):
    while True:
        choice = input(">> ")
        try:
            thing = int(choice)
            if 0<thing<=maxvalue-len(localexcept) or thing in localexcept:
                return thing
            else:
                error(0)
        except ValueError:
            if choice in globalexcept:
                return choice
            else:
                error(2)