import random
import numpy as np

global mackerel
global cockle
global s_karp



def fish_func_def (fishing, a):  #Defines the fishing function
    mackerel = 0
    cockle = 0
    s_karp = 0

    fishing = raw_input("""
Did you catch a fish?

1. Yes
2. No
3. Maybe

Enter the corresponder number: """)

    if fishing == "1":
        a = random.randint(1,10)
        print a
        if a in range(1,4):
            mackerel +=1
            print"You caught a mackerel. Can be caught at lvl 16 in Runescape."
            print"You have ",mackerel," mackerel."
        elif a in range(4,7):
            print"You caught a cockle. The cockle is a native to Goolwa, where you went as a child."
            cockle +=1
            print"You have ",cockle," cockle."            
        elif a in range(7,10):
            print"You found nothing unfortunately :("
        elif a == 10:
            s_karp +=1
            print"You caught a shiny Magikarp :D You won the lottery!"
            print"You have",s_karp,"shiny Magikarp."    
        else:
            fish_func_def ("","")
    elif fishing =="2":
        print "Party pooper. Perhaps try a different option?"
        fish_func_def ("","")
    elif fishing =="3":
        print "You pressed 3"

    else:
        fishing = raw_input("That is not a valid selection. Please try again: ")

fish_func_def("","") #call the fish_func_def function that we defined earlier
