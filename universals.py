import csv
import time
import json

class Item(object):
    """items"""
    def __init__(self, code, name, desc, exp, sale_p, buy_p, h2, h3,**kwargs):
        self.code = code
        self.name = name
        self.desc = desc
        self.exp = exp
        self.sale_p = sale_p
        self.buy_p = buy_p
        self.h2 = h2
        self.h3 = h3
        self.type = 'other'
    def __str__(self):
        return "Item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Item(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

class Fish(Item):
    def __init__(self,code,name,desc,exp,h1,sale_p,buy_p,h2,h3,**kwargs):
        super().__init__(code,name,desc,exp,sale_p,buy_p,h2,h3)
        self.type = 'fish'
        self.sell_price = 5
    def __str__(self):
        return "Fish item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Fish(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

class Bait(Item):
    def __init__(self,code,name,desc,exp,h1,sale_p,buy_p,h2,h3,**kwargs):
        super().__init__(code,name,desc,exp,sale_p,buy_p,h2,h3)
        self.type = 'bait'
    def __str__(self):
        return "Bait item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Bait(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

class Material(Item):
    def __init__(self,code,name,desc,exp,h1,sale_p,buy_p,h2,h3,**kwargs):
        super().__init__(code,name,desc,exp,sale_p,buy_p,h2,h3)
        self.type = 'material'
    def __str__(self):
        return "Material item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Material(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

ListOfItems = {}
with open('allitems_m.csv', 'r') as readfile:
    reader = csv.DictReader(readfile)
    for row in reader:
        if row['i_type'] == 'fish':
            ThisItem = Fish(**row)
            ListOfItems[ThisItem.code] = ThisItem
        elif row['i_type'] == 'bait':
            ThisItem = Bait(**row)
            ListOfItems[ThisItem.code] = ThisItem
        else:
            ThisItem = Item(**row)
        ListOfItems[ThisItem.code] = ThisItem

class Player(object):
    def __init__(self, username, password, createtime, lastlogin, exp, inventory, position,*args):
        self.username = username
        self.password = password
        self.createtime = createtime
        self.lastlogin = lastlogin
        self.exp = exp
        self.inventory = inventory
        self.position = position
        self.hsll = (time.time() - float(lastlogin))/3600
    def updatetime(self):
        self.lastlogin = int(time.time())
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
    def disp_currency(self, currency):
        print("You now have %s %s." % (self.inventory[currency],univ.ListOfItems[currency].name))
    def help_display(self):
        print("HELP\n")
    def inv_display(self): 
        print("YOUR INVENTORY:\n-------------------------")
        for key in self.inventory:
            print('%s: %s' % (univ.ListOfItems[key].name, self.inventory[key]))
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass

def error(number):
    print ("Error %s: That is invalid. Try again." % (number)) 

yes = ['yes','y','ya','ye','1','True']
no = ['no','na','n','0','False']
skills = ['fishing']

def IntChoice(maxvalue,globalexcept,localexcept):
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