import csv
import random

inv = {}

uname = raw_input ("What username?")

class User:
    # A User's account
    def __init__(self, f_j, mackerel, cockle, s_karp):
        self.f_j = f_j
        self.mackerel = mackerel
        self.cockle = cockle
        self.s_karp = s_karp
        print f_j
    def fish_away(self):
        while True:
            fish = raw_input("Would you like to fish? Press Y for yes, N for no.\n")
            print "Fish = ", fish, "."
            if fish == "Y" or "y":
                if self.f_j >0:
                    self.f_j -= 1
                    a = random.randint(1,10)
                    if a in range(1,4):
                        self.mackerel += 1
                        print"You caught a mackerel. Can be caught at lvl 16 in Runescape."
                        print "You have", self.mackerel, "mackerel"
                        self.suc_fish()
                    elif a in range(4,7):
                        self.cockle += 1
                        print"You caught a cockle. The cockle is a native to Goolwa, where you went as a child."
                        print"You have ", self.cockle, "cockle."
                        self.suc_fish()
                    elif a in range(7,10):
                        print"You found nothing unfortunately :("
                        self.suc_fish()
                    elif a == 10:
                        self.s_karp += 1
                        print"You caught a shiny Magikarp :D You won the lottery!"
                        print"You have", self.s_karp,"shiny Magikarp."
                        self.suc_fish()
                if self.f_j <=0:
                    print "You have no units of fishing juice left. Try waiting at least another hour."
            elif fish == "n" or "N":
                break
            else:
                print "Invalid response, try again.\n"
    def suc_fish(self):
        print "You have ", self.f_j, "fishing juice remaining."
        
uname = User(10,0,0,0)
uname.fish_away()
