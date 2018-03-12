import csv
import time
import json

class Item(object):
    """items"""
    def __init__(self,code,name,desc,exp,acceptP,vendP,**kwargs):
        self.code = code
        self.name = name
        self.desc = desc
        self.exp = int(exp)
        self.acceptP = int(acceptP) # shop buys from player
        self.vendP = int(vendP) # shop sells to player
        self.type = 'other'
    def __str__(self):
        return "Item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Item(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass

class Fish(Item):
    def __init__(self,code,name,desc,exp,acceptP,vendP,minlvl,**kwargs):
        super().__init__(code,name,desc,exp,acceptP,vendP,**kwargs)
        self.type = 'fish'
        self.min_lvl=minlvl
    def __str__(self):
        return "Fish item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Fish(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

class Bait(Item):
    def __init__(self,code,name,desc,exp,acceptP,vendP,**kwargs):
        super().__init__(code,name,desc,exp,acceptP,vendP)
        self.type = 'bait'
    def __str__(self):
        return "Bait item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Bait(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

class Material(Item):
    def __init__(self,code,name,desc,exp,acceptP,vendP,**kwargs):
        super().__init__(code,name,desc,exp,acceptP,vendP,**kwargs)
        self.type = 'material'
    def __str__(self):
        return "Material item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Material(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

ListOfItems = {}
with open('allitems_m.csv', 'r') as readfile:
    reader = csv.DictReader(readfile)
    for row in reader:
        if row['iType'] == 'fish':
            ThisItem = Fish(**row)
            ListOfItems[ThisItem.code] = ThisItem
        elif row['iType'] == 'bait':
            ThisItem = Bait(**row)
            ListOfItems[ThisItem.code] = ThisItem
        else:
            ThisItem = Item(**row)
        ListOfItems[ThisItem.code] = ThisItem

class Player(object):
    def __init__(self, username, password, createtime, lastlogin, exp, inventory, position,equipment,*args):
        self.username = username
        self.password = password
        self.createtime = createtime
        self.lastlogin = lastlogin
        self.exp = exp
        for skill in skills:
            self.exp[skill]=exp.get(skill,0)
        self.inventory={}
        for item in ListOfItems.keys():
            self.inventory[item]=inventory.get(item, 0)
        self.position = position
        self.hsll = (time.time() - float(lastlogin))/3600
        self.equipment=equipment
    def updatetime(self):
        self.lastlogin = int(time.time())
    def save(self):
        stats = {
        "username": self.username,
        "password": self.password,
        "createtime": self.createtime,
        "lastlogin": self.lastlogin,
        "exp":self.exp,
        "inventory":self.inventory,
        "position":self.position,
        "equipment":self.equipment
        }
        with open('./PlayerAccts/'+self.username+'_p.json', 'w') as file:
            json.dump(stats, file)
    def disp_currency(self, currency):
        print("You have %s %s." % (self.inventory[currency],ListOfItems[currency].name))
    def help_display(self):
        print("HELP\n")
    def relog(player):
        for item in player.equipment.items():
            print(ListOfItems[item].name)
        player.inventory['i00000']+=int(player.hsll)
    def inv_display(self): 
        print("YOUR INVENTORY:\n-------------------------")
        for key in self.inventory:
            print('%s: %s' % (ListOfItems[key].name, self.inventory[key]))
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass

def error(number):
    print ("Error %s: That is invalid. Try again." % (number)) 

yes = ['yes','y','ya','ye','1','True']
no = ['no','na','n','0','False','nah','nope']
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
            if choice.lower() in globalexcept:
                return choice.lower()
            else:
                error(2)

def updateDict(adict,actions,localexcept):
    length=len(adict-len(localexcept))
    for item in actions:
        adict[length+1]=item
        length+=1

# exptable = {10x^2 for x in range(1,1000)}y=15x^{2.4}+42