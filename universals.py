import csv
import time
import json
import itemClasses as ic

ListOfItems = {}
with open('allitems_m.csv', 'r') as readfile:
    reader = csv.DictReader(readfile)
    for row in reader:
        if row['iType'] == 'fish':
            ThisItem = ic.Fish(**row)
            ListOfItems[ThisItem.code] = ThisItem
        elif row['iType'] == 'bait':
            ThisItem = ic.Bait(**row)
            ListOfItems[ThisItem.code] = ThisItem
        elif row['iType'] == 'eqpt':
            ThisItem = ic.Equipment(**row)
            ListOfItems[ThisItem.code] = ThisItem
        else:
            ThisItem = ic.Item(**row)
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
    def relog(self):
        for slot,item in self.equipment.items():
            print(ListOfItems[item].name)
        self.inventory['i00000']+=int(self.hsll)
    def equip(self,item):
        try:
            if item.slot: # if !=0
                if self.equipment[item.slot]: #if the slot is currently full, remove the item currently in there
                    if item.code!=self.equipment[item.slot]:
                        confirm=input("Do you want to unequip %s and equip %s instead?\n>> "
                            %(ListOfItems[self.equipment[item.slot]].name,ListOfItems[item.code].name)).strip().lower()
                        if confirm in yes:
                            self.inventory[self.equipment[item.slot]]+=1
                            print("Returned %s back to inventory."%ListOfItems[self.equipment[item.slot]].name)
                            self.inventory[item.code]-=1
                            self.equipment[item.slot]=item.code
                            print("Equipped %s."%ListOfItems[item.code].name)
                    else:
                        print("You already have that item equipped.")
                else:
                    self.inventory[item.code]-=1
                    self.equipment[item.slot]=item.code
                    print("Equipped %s."%ListOfItems[item.code].name)
            else:
                print("This item cannot be equipped.")
        except KeyError as e:
            raise e
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
