import random
import csv
import time

class User_s:
    """user stats file for times and such."""
    def __init__(self, f_time_raw, p_time_raw, pword, delta, uname):
        self.f_time_raw = f_time_raw
        self.p_time_raw = p_time_raw
        self.pword = pword
        self.delta = delta
        self.uname = uname
    def get_init_times(self):
        with open(uname+'.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            stats = dict(reader)
            self.f_time_raw = stats["Create Time"]
            self.p_time_raw = stats["Last Login"]
            self.pword = stats["Password"]
            self.delta = float(stats["Last Login"]) - float(stats["Create Time"])
    def update_time(self):
        self.p_time_raw = time.time()
    def save(self):
        stats = {"Create Time":self.f_time_raw, "Last Login": self.p_time_raw, "Password":self.pword}
        with open(uname+'.csv', 'w') as gamefile: 
            writer = csv.writer(gamefile, dialect = 'excel')
            for key, value in stats.items():
                writer.writerow([key, value])

class User_g:
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
                    time.sleep(0.5)
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
        with open(uname+'_g_info.csv', 'w') as gamefile: 
            writer = csv.writer(gamefile, dialect = 'excel')
            for key, value in inv.items():
                writer.writerow([key, value])
    def load(self):
        with open(uname+'_g_info.csv', 'r') as csv_file:
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
                time.sleep(0.5)
                self.inv_display()
            elif menu =="2":
                time.sleep(0.5)
                self.fish_away()
            elif menu == "3":
                self.shop_display()
            elif menu == "4":
                self.help_display()
            elif menu == "5":
                print ("Saving and exiting game.")
                self.save()
                time.sleep(0.5)
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

        
player_s = User_s("","","","",uname) #update this to include from beginning
player_s.get_init_times()
print(player_s.delta)
print(player_s.p_time_raw)

f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(player_s.f_time_raw)))
p_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(player_s.p_time_raw)))
h_s_l_login = (float(time.time()) - float(player_s.p_time_raw))/3600 #make this a function of the player

if player_s.p_time_raw == 0: #If this is the first access of the game, then delta_t == 0
    time.sleep(1)
    player_s.update_time()
    player_s.save()
    player_g = User_g(10,0,0,0,uname)
    print ("Welcome to the game!\n"
           "Your very first login time: %s\n"
           "Hours since last login: %s\n" %(f_time, h_s_l_login))
    player_g.fish_away()
    
elif player_s.delta > 0: #If this is NOT the first access, then delta_t will not == 0 (we will have overwritten the current login time to be different from the initial time) - TBC
    player_g = User_g(0,0,0,0,uname)
    h_s_l_login
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
    player_g.fish_away()

elif player_s.delta < 0 and player_s.p_time_raw != 0: #not working for some reason: fix this.
    print("Error.")
    print(player_s.p_time_raw)