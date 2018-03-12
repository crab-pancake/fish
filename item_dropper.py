import random as rand
import json
import universals as univ

fishing_drop ={
1:["Treasure Chest", "Native pearl", "Tetrodotoxin cubes", "Hapalochleana egg"],
2:["Gummy sharkling", "Electric eel", "Flounder", "Magikarp", "Feebas"],
3:["Pufferfish", "Mackerel", "Shrimp", "Snapper", "Bass"]
}

rarity = [
("Unbelievably rare",1),
("Ultra rare",2),
("Rare",4),
("Uncommon",8),
("Common",16),
]

egg_drop = {
1: ["Wynaut"],
2: ["Azurill"],
3: ["Makuhita", "Mudkip", "Torchic", "Treecko", "Shroomish", "Slakoth"],
4: ["Skitty", "Ralts", "Seedot"],
5: ["Gulpin", "Poochyena", "Spoink", "Wurmple", "Zigzagoon"]
}

def load(level):
    while True:
        collect = input("How many times would you like to fish?\n >>")
        for d in range(int(collect)):     
            with open('./Locations/l0023_t.json', 'r') as file:
                loaded = json.load(file)
            length = len(loaded["items"])
            #create an empty 'pool'. The pool will be the items available to be received based upon the location (JSON) as well as the patient's level
            pool = []
            rarity_pool = 0
            for a in range(0,length):
                itemnamecode = loaded["items"][a]["code"]
                dog = univ.ListOfItems[itemnamecode]
                if level >= int(dog.h2): #Adds 'item' to the pool if the player's level is greater than 'h2' (placeholder for minimum level required. Found in allitems_m.csv)
                    pool.append(itemnamecode)
                    ## print("Your level of %s is sufficient that %s has been included in the pool (a level of %s is required)." % (level, dog.name, dog.h2))
                if level < int(dog.h2):
                    pass
                    ##print("Insufficient level. %s excluded." % (dog.name))

            #Using the 'pool' of items, we calculate the probability of each item dropping. This is based upon the rarity value provided in the location JSON file, with a rarity of 0 being guaranteed, and higher rarities being progresively rare
            pool_weights= {}    
            for b in range (0,len(pool)):
                for c in range (0, length):
                    if pool[b] == loaded["items"][c]["code"]:
                        rarity_pool += 2**(5 - loaded["items"][c]["rarity"])
                        pool_weights[pool[b]] = 2**(5 - loaded["items"][c]["rarity"])
            
            #Now 'regularise' the rarity pool, by assigning a probability to each item (i.e. a float from 0 to 1)
            for b in range (0,len(pool)):
                    pool_weights[pool[b]] = pool_weights[pool[b]]/rarity_pool

            #This final bit randomly selects the fish that is caught (based upon the weight given in the pool_weights dictionary).
            var = rand.random()
            ##print("Variable =" + str(var))
            s = 0
            for key in pool_weights:
                s += pool_weights[key]
                if s> var:
                    success = univ.ListOfItems[key]
                    print("You caught a %s. This has a %s catch rate for you at level %s." % (success.name, format(pool_weights[key],'.2f'), level))
                    break

def drop_item(skill, modifier, level, *bound):
    while True:
        fish = input("Would you like to fish?")
        if fish == 'y':    
            var = rand.random()
            for a in range (1,len(bound)+1):
                if var <= sum(bound[:a]):
                    print("You got a %s. This is a %s item."  % (rand.choice(skill[a]), rarity[len(bound)-a].lower()))
                    break

def drop_egg(skill):
    while True:
        collect = input("How many eggs would you like to collect? [Note: This is the Hoenn egg update only.]\n >>")
        for d in range(int(collect)):
            total_denominator = 0
            for a in range(0,len(skill)):
                total_denominator += rarity[a][1] * len(skill[a+1]) 
            var = rand.randint(1,total_denominator)
            total_denominator_t = 0
            for a in range(0,len(skill)):
                inc_denominator_t = rarity[a][1] * len(skill[a+1])
                total_denominator_t += inc_denominator_t
                if var <= total_denominator_t:
                    pokestats = {
                    1:["Attack",0],
                    2:["Defence",0],
                    3:["Stamina",0]
                    }
                    comments = ""
                    for b in range (1,3+1):
                        pokestats[b][1] = rand.randint(10,15)
                        if pokestats[b][1] == 15:
                            comments += ("Perfect stat in " + pokestats[b][0].lower()+". ")
                        if pokestats[1][1] == pokestats [2][1] == pokestats [3][1] == 15:
                            comments +=  ("THIS IS A PERFECT POKEMON. DO NOT TRANSFER TO NAZI WILLOW!!")
                    print("You collected a %s egg, a %s type of egg. Its stats are %s/%s/%s. %s" % (rand.choice(skill[a+1]), rarity[a][0].lower(), pokestats[1][1], pokestats[2][1], pokestats[3][1], comments))
                    break

if __name__ == '__main__':
    load(40)
    # drop_item(fishing_drop, 1.02, 10, 0.08, 0.09, 0.9)
    # drop_egg(egg_drop)
