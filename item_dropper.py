import random as rand

fishing_drop ={
1:["Treasure Chest", "Native pearl", "Tetrodotoxin cubes", "Hapalochleana egg"],
2:["Gummy sharkling", "Electric eel", "Flounder", "Magikarp", "Feebas"],
3:["Pufferfish", "Mackerel", "Shrimp", "Snapper", "Bass"]
}

rarity = [
"Common",
"Uncommon",
"Rare",
"Ultra rare",
"Unbelievably rare"
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
        collect = input("How many eggs would you like to collect an egg? [Note: This is the Hoenn egg update]\n >>")
        for d in range(int(collect)):        
            total_denominator = 0
            for a in range(1,len(skill)+1):
                inc_denominator = 2**(a-1) * len(skill[a])
                total_denominator += inc_denominator
            var = rand.randint(1,total_denominator)
            total_denominator_t = 0
            for a in range(1,len(skill)+1):
                inc_denominator_t = 2**(a-1) * len(skill[a])
                total_denominator_t += inc_denominator_t
                if var <= total_denominator_t:
                    print("You collected a %s egg. This is a %s type of egg." % (rand.choice(skill[a]), rarity[len(skill)-a].lower()))
                    break
        # if fish == 'y':    
        #     var = rand.random()
        #     for a in range (1,len(bound)+1):
        #         if var <= sum(bound[:a]):
        #             print("You got a %s. This is a %s item."  % (rand.choice(skill[a]), rarity[len(bound)-a].lower()))
        #             break

if __name__ == '__main__':
    # drop_item(fishing_drop, 1.02, 10, 0.08, 0.09, 0.9)
    drop_egg(egg_drop)
