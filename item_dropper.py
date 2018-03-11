import random as rand

fishing_drop ={
1:["Treasure Chest", "Native pearl", "Tetrodotoxin cube", "Hapalochleana egg"],
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

def drop_item(skill, drop_mod, *bound):
    while True:
        fish = input("Would you like to fish?")
        if fish == 'y':    
            var = rand.random()
            for a in range (1,len(bound)+1):
                if var <= sum(bound[:a]):
                    print("You got a %s. This is a %s item."  % (rand.choice(skill[a]), rarity[len(bound)-a].lower()))
                    break

if __name__ == '__main__':
    drop_item(fishing_drop, 1, 0.08, 0.09, 0.9)