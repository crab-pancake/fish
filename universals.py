import csv
import time
import json
import itemClasses as ic

Items = {}
RegenItems=[]
with open('allitems_m.json', 'r') as file:
    reader = json.load(file)
    for row in reader:
        if row['baseRegen']:
            RegenItems.append(row['code'])
        try:
            ThisItem=getattr(ic,row['iType'])(**row)
        except AttributeError as e:
            ThisItem=getattr(ic,"Item")(**row)
        Items[ThisItem.code]=ThisItem

class Player(object):
    """A player object"""
    def __init__(self,username,password,createtime,lastlogin,exp,inventory,position,equipment,**kwargs):
        self.username = username
        self.password = password
        self.createtime = createtime
        self.lastlogin = lastlogin
        self.exp = exp
        for skill in skills:
            self.exp[skill]=exp.get(skill,0)
        self.inventory={}
        for item in Items.keys():
            self.inventory[item]=inventory.get(item,0)
        self.position = position
        self.hsll = (time.time()-lastlogin)/3600
        self.equipment={int(k):v for k,v in sorted(equipment.items())}
    def updatetime(self):
        self.lastlogin = int(time.time())
    def save(self):
        with open('./PlayerAccts/'+self.username+'_p.json', 'w') as file:
            json.dump(self.__dict__, file)
    def disp_currency(self, currency):
        print("You have %s %s."%(self.inventory[currency],Items[currency].name))
    def equip(self,item):
        try:
            if item.slot: # if !=0
                if self.equipment[item.slot]: #if the slot is currently full, remove the item currently in there
                    if item.code!=self.equipment[item.slot]:
                        confirm=input("Do you want to unequip %s and equip %s instead? (Y/N)\n>> "
                            %(Items[self.equipment[item.slot]].name,Items[item.code].name)).strip().lower()
                        if confirm in yes:
                            self.inventory[self.equipment[item.slot]]+=1
                            print("Returned %s back to inventory."%Items[self.equipment[item.slot]].name)
                            self.inventory[item.code]-=1
                            self.equipment[item.slot]=item.code
                            print("Equipped %s."%Items[item.code].name)
                    else:
                        print("You already have that item equipped.")
                else:
                    self.inventory[item.code]-=1
                    self.equipment[item.slot]=item.code
                    print("Equipped %s."%Items[item.code].name)
            else:
                print("This item cannot be equipped.")
        except KeyError as e:
            raise e
    def unequip(self,slot):
        if self.equipment[slot]:
            choice=input("Do you want to unequip your %s?\n>> "%Items[self.equipment[slot]].name).strip().lower()
            if choice in yes:
                self.inventory[self.equipment[slot]]+=1
                print("Your %s has been unequipped. You now have an empty slot %s."%(Items[self.equipment[slot]].name,slot))
                self.equipment[slot]=None
        else:
            print("You don't have anything equipped in that slot.")
    def inv_display(self): 
        print("YOUR INVENTORY:\n-------------------------")
        for key in self.inventory:
            print('%s: %s' % (Items[key].name.ljust(20), self.inventory[key]))
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

class InputError(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

with open('errors_m.csv','r') as file:
    reader = dict(csv.reader(file))
    Errors=reader

def updateDict(adict,actions,localexcept):
    length=len(adict-len(localexcept))
    for item in actions:
        adict[length+1]=item
        length+=1

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

# exptable = {10x^2 for x in range(1,1000)}y=15x^{2.4}+42