import random as rand
import json
import universals as univ
import time

rarity_new = [
("Unbelievably rare",1),
("Ultra rare",2),
("Rare",3),
("Uncommon",4),
("Common",5),
]

egg_drop = {
1: ["Wynaut"],
2: ["Azurill"],
3: ["Makuhita", "Mudkip", "Torchic", "Treecko", "Shroomish", "Slakoth"],
4: ["Skitty", "Ralts", "Seedot"],
5: ["Gulpin", "Poochyena", "Spoink", "Wurmple", "Zigzagoon"]
}

def load(player):
    level = (player.exp['fishing'])/10
DropTable = {}
    #Load up the location's available item drops
    with open('./Locations/l0023_t.json', 'r') as file:
        reader = json.load(file)["items"]

    #Create rarity denominator and create the rarity drop table. Uncommon items are two as rare as common items etc
    for a in range(len(rarity_new)):
        DropTable[a+1]=[]

    #Load up items suitable for the player's level
    for a in range(0,len(reader)):
        itemnamecode = reader[a]["code"]
        if level >= univ.ListOfItems[itemnamecode].min_lvl: #Adds 'item' to the pool if the player's level is greater than 'min_lvl' Found in allitems_m.csv)
            DropTable[reader[a]["rarity"]].append(itemnamecode)

    collect = int(input("How many times would you like to fish?\n>> "))

    while collect>0:
        collect-=1
        tier = 0
        var = rand.randint(0,rarity_new[-1][1])
        for a in range(len(rarity_new),0,-1): # Counts backwards from Common
            if var < 2**rarity_new[a][1]
            if s> var:
                if not DropTable[len(rarity_new)-a]:
                    tier = len(rarity_new)-a-1
                    print("Rarity class decreased. Rarity class = %s" % (tier))
                    break
                else:
                    tier = len(rarity_new)-a
                    print("Rarity class = %s" % (tier))
                    break
                break
        gained_item_code = rand.choice(DropTable[tier])
        gained_item_name = univ.ListOfItems[gained_item_code].name
        player.inventory[gained_item_code]+=1
        print("You gained a %s. You have %s %s." % (gained_item_name, player.inventory[gained_item_code], gained_item_name))

if __name__ == '__main__':
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(**reader)
    while True:
        load(player)



    # drop_item(fishing_drop, 1.02, 10, 0.08, 0.09, 0.9)
    # drop_egg(egg_drop)
