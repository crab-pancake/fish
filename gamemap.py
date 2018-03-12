import csv
import json
import universals as univ
import random
import time
import ingameMenu

def displayPlaces(player):
    with Locations[player.position] as pos:
        print("You are currently at %s." % (pos.name))
        while True:
            print("Which place do you want to go into?")
            for num, place in sorted(pos.places.items())[1:]:
                print(num, pos.places[num][0])
            print(0, pos.places[0][0])
            choice=univ.IntChoice(len(pos.places),['x','m', 'q'],[0])
            if choice == 'x' or choice == 0:
                return (player, travel)
            elif choice == 'q':
                print("Quitting...")
                return (player, quit)
            elif choice == 'm':
                return ingameMenu.menu(player)
            else: 
                return (player,pos.places[choice][1].takeaction)

def travel(player):
    with Locations[player.position] as pos:
        print("You are leaving %s."%(pos.name))
        traveller = {0:'Return'}
        print('Type the number of the town you want to travel to.')
        for num, location in enumerate(sorted(pos.destinations),1):
            traveller[num] = Locations[location.strip()].name
            print(num,Locations[location.strip()].name)
        print(0,traveller[0])
        while True:
            choice=univ.IntChoice(len(traveller), ['x','q','m'], [0])
            if choice == 0 or choice == 'x':
                print('Returning to %s...'%(pos.name))
                return (player, displayPlaces)
            elif choice == 'q':
                print("Quitting...")
                return (player, quit)
            elif choice == 'm':
                action=ingameMenu.menu(player)
                if action:
                    return action
            else:
                player.position = sorted(pos.destinations)[choice-1]
                print('You have moved to %s.'%(Locations[player.position].name))
                print(Locations[player.position].desc)
                return (player, displayPlaces)

def quit(player):
    answer = input("Are you sure you want to quit? Type yes to confirm, or anything else to cancel.\n>> ").strip().lower()
    if answer in univ.yes:
        print("Thanks for playing, see you again soon.")
        return (player, None)
    else:
        print("Cancelled, returning to game.")
        return (player, displayPlaces)

class Location(object):
    def __init__(self,code,name,desc,travelling,**kwargs):
        self.code = code
        self.name = name
        self.desc = desc
        self.places = {0:('Leave', travel)}
        with open('./locations/'+self.code+'_l.csv', 'r') as file:
            reader = csv.DictReader(file)
            for num,row in enumerate(reader,1):
                if row['type'] == 'shop':
                    self.places[num] = (row['name'], Shop(**row))
                elif row['type'] == 'FishSpot':
                    self.places[num] = (row['name'], FishSpot(**row))
        self.destinations = travelling.split(';')
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass

class Place(object):
    def __init__(self,code,name,description,**kwargs):
        self.code = code
        self.name = name
        self.description = description
        self.actions = {0:('Leave', self.leave)}
    def takeaction(self,player):
        while True:
            print("\nWhat do you want to do?")
            for key, val in sorted(self.actions.items())[1:]:
                print(key, val[0])
            print(0, self.actions[0][0])
            choice=univ.IntChoice(len(self.actions),['x','m','q'],[0])
            if choice == 'q':
                print("Quitting...")
                return (player, quit)
            elif choice == 'x' or choice == 0:
                return self.leave(player)
            elif choice == 'm':
                action=ingameMenu.menu(player)
                if action:
                    return action
            else:
                self.actions[choice][1](player) # value of [choice] key in self.actions, 2nd entry (always a func), called with (player) as parameter
    def leave(self, player):
        print("Leaving...")
        return (player, displayPlaces)
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass

class Shop(Place):
    """Class for shops selling different things."""
    def __init__(self,code,name,desc,IntroLine,ExitLine,currency,**kwargs):
        super().__init__(code,name,desc)
        self.intro = IntroLine
        self.exit = ExitLine
        self.vendList=[]
        self.acceptList=[]
        self.stock={}
        self.lasttime=0
        with open('./locations/'+self.code+"_s.json", 'r') as file:
            reader = json.load(file)
            self.lasttime=reader['lasttime']
            self.stock=reader['stock']
            for item in reader['accepts']:
                try:
                    self.acceptList.append((item['code'],item['price']))
                except KeyError:
                    self.acceptList.append((item['code'],univ.ListOfItems[item['code'].acceptP]))
            for item in reader['vends']:
                try:
                    self.vendList.append((item['code'],item['price']))
                except KeyError:
                    self.vendList.append((item['code'],univ.ListOfItems[item['code'].vendP]))
        self.currency=currency
        self.actions.update({1:("Sell your items",self.accept),2:("Buy from the store",self.vend)})  # 1:('Shopfront', self.shopfront),
    # def shopfront(self, player):
    #     print(self.intro)
    #     self.shopactions={1:("Sell your items",self.accept),2:("Buy from the store",self.vend),0:("Leave",self.leave)}
    #     while True:
    #         print("What would you like to do?")
    #         for key in self.thisactions:
    #             print(key, self.thisactions[key][0])
    #         choice = univ.IntChoice(3, ['q','x'], [0])
    #         if choice == "q":
    #             return (player, quit)
    #         elif choice == "x" or choice==0:
    #             print(self.exit)
    #             return (player,displayPlaces)
    #         else: self.thisactions[choice][1](player)
    def update(self):
        with open('./locations/'+self.code+"_s.json", 'r') as file:
            reader = json.load(file)
            reader['lasttime']=int(time.time())
            reader['stock']=self.stock
            with open('./locations/'+self.code+"_s.json", 'w') as file:
                json.dump(reader,file)
    def accept(self,player):
        while True:
            print("\nYou can sell the following items here:\n")
            selldict={0:'Leave'}
            for num, key in enumerate(self.acceptList,1):
                selldict[num]=key
                print(num,"%s: %sx    Sale price: %s each"%(univ.ListOfItems[key[0]].name,player.inventory[key[0]], key[1])) # key[1] is the price
            print(0, selldict[0])
            print('Which item would you like to sell?')
            choice=univ.IntChoice(len(selldict),['x'],[0])
            if choice == 'x' or choice==0:
                break
            else:
                key=selldict[choice]
                while True:
                    print("The shop has %s [ %s ]"%(self.stock[key[0]], univ.ListOfItems[key[0]].name))
                    try:
                        sale_q=int(input("How many [ %s ] do you want to sell? Max: [ %s ] Sale price: [ %s ] %s\n>> "
                            %(univ.ListOfItems[key[0]].name,player.inventory[key[0]], key[1],univ.ListOfItems[self.currency].name)))
                        if 0<=sale_q<=player.inventory[key[0]]:
                            player.inventory[key[0]]-=sale_q
                            try:
                                self.stock[key[0]]+=sale_q
                            except KeyError:
                                self.stock.update({key[0]:sale_q})
                            self.update()
                            player.inventory[self.currency] += sale_q*key[1]
                            print("You now have %s %s." % (player.inventory[key[0]], univ.ListOfItems[key[0]].name))
                            player.disp_currency(self.currency)
                            player.save()
                            break
                        else:
                            univ.error(1)
                    except ValueError:
                        univ.error(2)
    def vend(self,player):
        print("The shop has the following items for sale:")
        buydict={0:"Leave"}
        for num, key in enumerate(self.vendList,1):
            buydict[num]=key
            print(num,"%s: %s"%(univ.ListOfItems[key[0]].name,key[1]))
        print(0,buydict[0])
        player.disp_currency(self.currency)
        while True:
            print("Which item would you like to buy? 'x' to return")
            choice=univ.IntChoice(len(buydict),['x'],[0])
            if choice == 'x' or choice==0:
                break
            else:
                with univ.ListOfItems[buydict[choice][0]]as buyitem:
                    while True:
                        buy_q = input("How many [ %s ] would you like to purchase? Purchase price: [ %s ] %s. 'x' to cancel\n>> " % (buyitem.name,buydict[choice][1],univ.ListOfItems[self.currency].name))
                        if buy_q == 'x':
                            break
                        try:
                            quantity = int(buy_q)
                            if player.inventory[self.currency] < quantity*buydict[choice][1]:
                                print("You don't have enough money for that. ")# univ.error(0)
                            else:
                                player.inventory[buyitem.code] += quantity
                                player.inventory[self.currency] -= quantity*buydict[choice][1]
                                print("You now have %s %s." % (player.inventory[buyitem.code],buyitem.name))
                                player.disp_currency(self.currency)
                                # player.save()
                                break
                        except ValueError:
                            univ.error(0)
                        break

class TrainingSpot(Place):
    """Superclass for skill training spots"""
    def __init__(self,code,name,description,skill,reqEquip,reqMats,min_lvl,failline,action,**kwargs):
        super().__init__(code,name,description)
        self.min_lvl=int(min_lvl)
        self.skill=skill
        self.reqEquip=reqEquip
        self.reqMats={k:int(v) for k,v in (i.split(':') for i in reqMats.strip("[]").split(';'))} #Get a string of form [k1:v1;k2:v2] and turn it into a dict
        self.loottable='./locations/'+code+'_t.csv'
        self.failline=failline
        self.action=action
        self.actions.update({1:(self.action.title()+"!", self.TrainSkill)})
    def TrainSkill(self, player):
        if player.exp[self.skill] < self.min_lvl: #*univ.levelmult
            print("Your [ %s ] level isn't high enough to %s here.\n")%(self.skill.title(),self.action)
            print("The minimum level for this spot is %s, your level is [ %s ]."%(self.min_lvl,player.exp[self.skill]))#exp must be divided by levelmult eventually
            return (player, displayPlaces)
        missingequip=[]
        #for slot in self.reqEquip:
            # if player.equipment[slot] != self.reqEquip[slot]:
                # missingequip.append(self.reqEquip[slot])
        if len(missingequip):
            print("You don't have the required equipment to work here. You still need:")
            for item in missingequip:
                print("- %s "%(univ.ListOfItems[item].name))
        else:
            with open(self.loottable,'r') as file:
                reader=dict(csv.reader(file))
                while True:
                    choice=input("Do you want to %s here? (Y/N)\n>> "%(self.action)).strip().lower()
                    if choice in univ.yes:
                        enoughStuff=True
                        for item in self.reqMats:
                            if player.inventory[item] < self.reqMats[item]:
                                enoughStuff=False
                                print("You don't have enough [ %s ].\n"
                                      "Required: %s\n"
                                      "Your inventory: %s"%(univ.ListOfItems[item].name, self.reqMats[item],player.inventory[item]))
                                return (player,displayPlaces)
                        if enoughStuff:
                            success=False# dropper(player,self.loottable)
                            rng=random.randint(0,100)
                            for item in reader:
                                if rng>=int(reader[item]):
                                    success=True
                                    player.inventory[item]+=1
                                    print(self.successline(player,item))
                                    print("You gained [ %s ] %s experience. "%(univ.ListOfItems[item].exp,self.skill))
                                    break
                            if not success:
                                print(self.failline)
                            for item in self.reqMats:
                                player.inventory[item] -= self.reqMats[item]
                                print("You have [ %s ] %s remaining."%(player.inventory[item],univ.ListOfItems[item].name))
                            player.save()
                    elif choice in univ.no:
                        return (player,displayPlaces)
                    else: univ.error(0)

class FishSpot(TrainingSpot):
    """Class for fishing spots."""
    def __init__(self,code,name,desc,reqEquip,reqMats,min_lvl,**kwargs):
        self.skill='fishing'
        self.failline="You didn't manage to catch anything."
        self.action="fish"
        super().__init__(code,name,desc,self.skill,reqEquip,reqMats,min_lvl,self.failline,self.action)
        # self.weather = weather  # add this later
    def successline(self,player,item):
        return "You successfully caught a %s!\nYou now have %s %s."%(univ.ListOfItems[item].name,player.inventory[item],univ.ListOfItems[item].name)

Locations = {}

with open('locations_l.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        location = Location(**row)
        Locations[row['code']] = location

if __name__ == "__main__":
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(**reader)
    nextAction = displayPlaces
    while True:
        returned = nextAction(player)
        player = returned[0]
        prevAction=nextAction
        nextAction = returned[1]
        player.save()
        if nextAction == None:
            break
        elif nextAction=="prev":
            nextAction=prevAction
        else:
            myTuple=nextAction

