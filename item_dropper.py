import random as rand

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
                    1:["Attack",0,""],
                    2:["Defence",0,""],
                    3:["Stamina",0,""]
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
    # drop_item(fishing_drop, 1.02, 10, 0.08, 0.09, 0.9)
    drop_egg(egg_drop)
