import random
import csv
import time

print('uname:',uname)

class User_s(object):
    """user stats file for times and such."""
    def __init__(self, f_time_raw, p_time_raw, pword, delta, uname):
        self.f_time_raw = f_time_raw
        self.p_time_raw = p_time_raw
        self.pword = pword
        self.delta = delta
        self.uname = uname
    #def get_init_times(self):
    #    with open(uname+'.csv', 'r') as csv_file:
    #        reader = csv.reader(csv_file)
    #        stats = dict(reader)
    #        self.f_time_raw = stats["Create Time"]
    #        self.p_time_raw = stats["Last Login"]
    #        self.pword = stats["Password"]
    #        self.delta = int(stats["Last Login"]) - int(stats["Create Time"])
    def update_time(self):
        self.p_time_raw = time.time()
    def save(self):
        stats = {"Create Time":self.f_time_raw, "Last Login": self.p_time_raw, "Password":self.pword}
        with open(self.uname+'.csv', 'w', newline='') as gamefile: 
            writer = csv.writer(gamefile, dialect='excel')
            for key, value in stats.items():
                writer.writerow([key, value])

class User_g(object):
    """ A User's account. Defines the amount of fishing juice and starting items."""
    def __init__(self, f_j, mackerel, cockle, s_karp, uname):
        self.f_j = f_j
        self.mackerel = mackerel
        self.cockle = cockle
        self.s_karp = s_karp
        self.uname = uname
    def fish_away(self):
        while True:
            fish = input("Would you like to fish? Press Y for yes, N for no.\n").lower()
            print ("Fish =",fish+".")
            if fish == "y":
                if self.f_j >0:
                    self.f_j -= 1
                    a = random.randint(1,10)
                    if a in range(1,4):
                        self.mackerel += 1
                        print("You caught a mackerel. Can be caught at lvl 16 in Runescape.")
                        print ("You have", self.mackerel, "mackerel")
                        self.suc_fish()
                    elif a in range(4,7):
                        self.cockle += 1
                        print("You caught a cockle. The cockle is a native to Goolwa, where you went as a child.")
                        print("You have", self.cockle, "cockle.")
                        self.suc_fish()
                    elif a in range(7,10):
                        print("You found nothing unfortunately :(")
                        self.suc_fish()
                    elif a == 10:
                        self.s_karp += 1
                        print("You caught a shiny Magikarp :D You won the lottery!")
                        print("You have", self.s_karp,"shiny Magikarp.")
                        self.suc_fish()
                if self.f_j <=0:
                    print ("You have no units of fishing juice left. Try waiting at least another hour.")
            elif fish == "n":
                break
            else:
                print ("Invalid response, try again.\n")
    def suc_fish(self):
        print ("You have ", self.f_j, "fishing juice remaining.")
        self.save()
    def save(self):
        inv = {"f_j":self.f_j, "mackerel": self.mackerel, "cockle": self.cockle, "s_karp": self.s_karp}
        with open(self.uname+'_g_info.csv', 'w', newline='') as gamefile: 
            writer = csv.writer(gamefile, dialect = 'excel')
            for key, value in inv.items():
                writer.writerow([key, value])
    def load(self):
        with open(self.uname+'_g_info.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            inv = dict(reader)
            self.f_j = int(inv["f_j"])
            self.mackerel = int(inv["mackerel"])
            self.cockle = int(inv["cockle"])
            self.s_karp = int(inv["s_karp"])
    def shop_display(self):
        print("Coles")
    def help_display(self):
        print("help me pls")
    def display_menu(self):
    	while True:
            menu = input("\nMENU\n"
                    "----------------------------\n"
                    "1. Display inventory\n"
                    "2. Fish!\n"
                    "3. Visit shop (sell and buy items)\n"
                    "4. Help\n"
                    "5. Exit game\n")
            if menu =="1":
                self.inv_display()
            elif menu =="2":
                self.fish_away()
            elif menu == "3":
                self.shop_display()
            elif menu == "4":
                self.help_display()
            elif menu == "5":
                print ("Saving and exiting game.")
                self.save()
                print ("Complete.")
                break
            else:
                self.error_message()
    def error_message(self):
        print ("Try again.")
    def inv_display(self): 
        print ("YOUR INVENTORY:\n"
               "-------------------------\n"
               "Fishing juice: {}\nMackerel: {}\nCockles: {} \nShiny Magikarp: {}".format(self.f_j, self.mackerel, self.cockle, self.s_karp))

player_s = User_s(stats["Create Time"],
                  stats["Last Login"],
                  stats["Password"],
                  float(stats["Last Login"]) - float(stats["Create Time"]),
                  uname)
print('delta:',player_s.delta)
print(player_s.p_time_raw,"ptimeraw")

f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(player_s.f_time_raw)))
p_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(player_s.p_time_raw)))
h_s_l_login = (float(time.time()) - float(player_s.p_time_raw))/3600 #make this a function of the player

if player_s.delta == 0: #If this is the first access of the game, then ptimeraw == 0
    print('running first mode')
    player_s.update_time()
    player_s.save()
    player_g = User_g(10,0,0,0,uname)
    print ("Welcome to the game!\n"
           "Your very first login time: %s\n"
           "Hours since last login: %s\n" %(f_time, h_s_l_login))
    player_g.display_menu()

elif player_s.delta > 0: 
    print('running second mode')
    player_g = User_g(0,0,0,0,uname)
    print(h_s_l_login)
    player_s.update_time()
    player_s.save()
    player_g.load()
    player_g.f_j += int(h_s_l_login)
    print(player_g.f_j)
    print ("___________________\n"
           "Welcome back to the game!\n"
           "Your very first login time: %s\n"
           "Hours since last login: %s\n\n"
           "Blocks of fishing juice you've acquired since the last login: %s\n\n"
           "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n\n" %(f_time, h_s_l_login, int(h_s_l_login)))
    player_g.display_menu()

elif (player_s.delta < 0 and player_s.p_time_raw): #not working for some reason: fix this.
    print("running error mode")
    print(player_s.p_time_raw)
    print(bool(player_s.p_time_raw))
    print(player_s.p_time_raw)