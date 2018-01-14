import random
import numpy as np


a = ""
encounter = ""


def fish_func_def (fishing, a):  #Defines the fishing function
    fishing = input("""
Did you catch a fish?

1. Yes
2. No
3. Maybe

Enter the corresponder number: """)

    if fishing == 1:
        a = random.randrange(1,10)
        print a
        if a in range(1,3):
            print"You caught a mackerel. Can be caught at lvl 10 in Runescape."
        if a in range(3,7):
            print"You caught a cockle. The cockle is a native to Goolwa, where you went as a child."
        if a in range(7,9):
            print"You found nothing unfortunately :("
        if a == 10:
            print"You caught a shiny Magikarp :D You won the lottery!"
        else:
            fish_func_def ("","")
    elif fishing ==2:
        print "Party pooper. Perhaps try a different option?"
        fish_func_def ("","")
    elif fishing ==3:
        print "You pressed 3"

    else:
        fishing = input("That is not a valid selection. Please try again: ")

fish_func_def("","") #call the fish_func_def function that we defined earlier
