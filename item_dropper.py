import random as rand
import json
import universals as univ
import time

fishing_drop ={
1:["Treasure Chest", "Native pearl", "Tetrodotoxin cubes", "Hapalochleana egg"],
2:["Gummy sharkling", "Electric eel", "Flounder", "Magikarp", "Feebas"],
3:["Pufferfish", "Mackerel", "Shrimp", "Snapper", "Bass"]
}

rarity_new = [
("Unbelievably rare",1),
("Ultra rare",2),
("Rare",3),
("Uncommon",4),
("Common",5),
]

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

def load(player):
    level = (player.exp['fishing'])/10
    rarity_drop_odds = {}
    rarity_drop_table = {}
    while True:
        #Create rarity denominator and create the rarity drop table. Uncommon items are two as rare as common items etc.
        rarity_denominator = 0
        for a in range(0,len(rarity_new)):
            rarity_denominator +=  2**rarity_new[a][1]
            rarity_drop_table[a+1] = []
        for a in range(0,len(rarity_new)):
            rarity_drop_odds[rarity_new[a][1]] = (2**(a+1))/rarity_denominator

        #Load up the location's available item drops
        with open('./Locations/l0023_t.json', 'r') as file:
            loaded = json.load(file)
            length = len(loaded["items"])

        #Load up items suitable for the player's level
        for a in range(0,length):
            itemnamecode = loaded["items"][a]["code"]
            dog = univ.ListOfItems[itemnamecode]
            if level >= int(dog.h2): #Adds 'item' to the pool if the player's level is greater than 'h2' (placeholder for minimum level required. Found in allitems_m.csv)
                rarity_drop_table[loaded["items"][a]["rarity"]].append(itemnamecode)

        collect = input("How many times would you like to fish?\n >>")

        for d in range(int(collect)):
            rarity_class = 0    
            var = rand.random()
            # print("var = %s" % (var))
            # print(rarity_drop_odds)
            s = 0
            # print(rarity_drop_table)
            for a in range(1,len(rarity_drop_odds)+1):
                s += rarity_drop_odds[a]
                # print(s)
                if s> var:
                    # print("S is bigger than var now.")
                    if rarity_drop_table[(5+1)-a] == []:
                        rarity_class = (5+1)-a-1
                        print("Rarity class decreased. Rarity class = %s" % (rarity_class))
                        break
                    else:
                        rarity_class = (5+1)-a
                        print("Rarity class = %s" % (rarity_class))
                        break
                    break
            gained_item_code = rand.choice(rarity_drop_table[rarity_class])
            gained_item_name = univ.ListOfItems[gained_item_code].name
            player.inventory[gained_item_code]+=1
            print("You gained a %s. You have %s %s." % (gained_item_name, player.inventory[gained_item_code], gained_item_name))

                    #     if rarity_drop_table[loaded["items"][a-b]["rarity"]] != []:
                    #         rarity_class = a
                    #         print(rarity_class)
                    # break
            # gained_item_name = univ.ListOfItems[rand.choice(rarity_drop_table[rarity_class])].name
            # print("You got a %s." % (rand.choice(rarity_drop_table[rarity_class])))
                    # success = univ.ListOfItems[key]

            #create an empty 'pool'. The pool will be the items available to be received based upon the location (JSON) as well as the patient's level


            # pool = []
            # rarity_pool = 0
            # for a in range(0,length):
            #     itemnamecode = loaded["items"][a]["code"]
            #     dog = univ.ListOfItems[itemnamecode]
            #     if level >= int(dog.h2): #Adds 'item' to the pool if the player's level is greater than 'h2' (placeholder for minimum level required. Found in allitems_m.csv)
            #         pool.append(itemnamecode)
            #         ## print("Your level of %s is sufficient that %s has been included in the pool (a level of %s is required)." % (level, dog.name, dog.h2))

            #         ##print("Insufficient level. %s excluded." % (dog.name))

            # #Using the 'pool' of items, we calculate the probability of each item dropping. This is based upon the rarity value provided in the location JSON file, with a rarity of 0 being guaranteed, and higher rarities being progresively rare
            # pool_weights= {}    
            # for b in range (0,len(pool)):
            #     for c in range (0, length):
            #         if pool[b] == loaded["items"][c]["code"]:
            #             rarity_pool += 2**(5 - loaded["items"][c]["rarity"])
            #             pool_weights[pool[b]] = 2**(5 - loaded["items"][c]["rarity"])
            
            # #Now 'regularise' the rarity pool, by assigning a probability to each item (i.e. a float from 0 to 1)
            # for b in range (0,len(pool)):
            #         pool_weights[pool[b]] = pool_weights[pool[b]]/rarity_pool

            # #This final bit randomly selects the fish that is caught (based upon the weight given in the pool_weights dictionary).
            # var = rand.random()
            # ##print("Variable =" + str(var))
            # s = 0
            # for key in pool_weights:
            #     s += pool_weights[key]
            #     if s> var:
            #         success = univ.ListOfItems[key]
            #         print("You caught a %s. This has a %s catch rate for you at level %s." % (success.name, format(pool_weights[key],'.2f'), level))
            #         break

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

def ray_catcher():
    print("You are catching a Rayquaza. Put in the following inputs to simulate the Rayquaza catching.")
    bonus_candy =1 
    balls = int(input("How many balls did you receive? (Max: 14)"))

    berry_input = int(input("What berry do you use?\n"
                        "1. Pinap\n"
                        "2. Razz berry\n"
                        "3. Golden Razz berry"))

    if berry_input == 1:
        berry = 1
        bonus_candy = 2
    elif berry_input == 2:
        berry = 1.5
    elif berry_input == 3:
        berry = 2.5
    else:
        print("Invalid response.")

    curve_input = int(input("Do you curve your throws?\n"
                        "1. Yes\n"
                        "2. No\n"))

    if curve_input == 1:
        curve = 1.7
    elif curve_input == 2:
        curve = 1
    else:
        print("Invalid response.")

    circle_input = int(input("What kind of description is your throw?\n"
                        "1. None\n"
                        "2. Nice!\n"
                        "3. Great!\n"
                        "4. Excellent!\n"))

    if circle_input == 1:
        circle = 1
    elif circle_input == 2:
        circle = 1.15
    elif circle_input == 3:
        circle = 1.55
    elif circle_input == 4:
        circle = 1.7
    else:
        print("Invalid response.")

    bcr = 0.02

    while True:
        hello = input("Ready to try and catch? Press enter if you are ready.")
        text = ""
        for a in range(1,balls+1):
            var = rand.random()
            catch_failure = (1 - bcr)**berry**curve**circle
            if var > catch_failure:
                print("You caught the Rayquaza! You caught it after %s throws. You would have got %s candy." % (a, 3*bonus_candy))
                break
            if var < catch_failure:
                print("You failed to catch the Rayquaza...")

if __name__ == '__main__':
    reader=''
    with open('./PlayerAccts/test_acct_p.json', 'r') as file:
        reader = json.load(file)
    player = univ.Player(**reader)
    load(player)



    # drop_item(fishing_drop, 1.02, 10, 0.08, 0.09, 0.9)
    # drop_egg(egg_drop)
