import random
import csv
import time

class User_s:
    def __init__(self, f_time_raw, p_time_raw, pword, delta, uname):
        self.f_time_raw = f_time_raw
        self.p_time_raw = p_time_raw
        self.pword = pword
        self.delta = delta
        self.uname = uname
    def get_init_times(self):
        with open(uname+'.csv', 'rb') as csv_file:
            reader = csv.reader(csv_file)
            stats = dict(reader)
            self.f_time_raw = stats["Create Time"]
            self.p_time_raw = stats["Last Login"]
            self.pword = stats["Password"]
    def update_time(self):
        self.p_time_raw = time.time()
    def delta_time(self): #works
        self.delta = float(self.p_time_raw) - float(self.f_time_raw)
    def save(self):
        stats = {"Create Time":self.f_time_raw, "Last Login": self.p_time_raw, "Password":self.pword}
        with open(uname+'.csv', 'wb') as gamefile: 
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
            fish = raw_input("Would you like to fish? Press Y for yes, N for no.\n").lower()
            print "Fish = ", fish, "."
            if fish == "y":
                if self.f_j >0:
                    self.f_j -= 1
                    a = random.randint(1,10)
                    time.sleep(0.5)
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
            elif fish == "n":
                self.display_menu()
                break
            else:
                print "Invalid response, try again.\n"
    def suc_fish(self):
        print "You have ", self.f_j, "fishing juice remaining."
        self.save()
    def save(self):
        inv = {"f_j":self.f_j, "mackerel": self.mackerel, "cockle": self.cockle, "s_karp": self.s_karp}
        with open(uname+'_g_info.csv', 'wb') as gamefile: 
            writer = csv.writer(gamefile, dialect = 'excel')
            for key, value in inv.items():
                writer.writerow([key, value])
    def load(self):
        with open(uname+'_g_info.csv', 'rb') as csv_file:
            reader = csv.reader(csv_file)
            inv = dict(reader)
            self.f_j = int(inv["f_j"])
            self.mackerel = int(inv["mackerel"])
            self.cockle = int(inv["cockle"])
            self.s_karp = int(inv["s_karp"])
    def display_menu(self):
        menu_input = input ("\nMENU\n"
                "----------------------------\n"
                "1. Display inventory\n"
                "2. Fish!\n"
                "3. Visit shop (sell and buy items)\n"
                "4. Help\n"
                "5. Exit game\n")
        if menu_input == 1:
            time.sleep(0.5)
            self.inv_display()
        if menu_input ==2:
            time.sleep(0.5)
            self.fish_away()
    ##    if menu_input == 3:
    ##        shop_display
    ##    if menu_input == 4:
    ##        help_display
        elif menu_input == 5:
            print "Saving and exiting game."
            self.save()
            time.sleep(0.5)
            print "Complete."
        else:
            self.error_message()
    def error_message(self):
        print "That's not a valid option. Try a different option, you nincompoop."
        self.display_menu()
    def inv_display(self): 
        print ("YOUR INVENTORY:\n"
               "-------------------------\n"
               "Fishing juice: {}\nMackerel: {}\nCockles: {} \nShiny Magikarp: {}".format(self.f_j, self.mackerel, self.cockle, self.s_karp))

        
player_s = User_s("","","","",uname)
player_s.get_init_times()
player_s.delta_time()
print player_s.delta

f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(player_s.f_time_raw)))
p_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(player_s.p_time_raw)))
h_s_l_login = (float(time.time()) - float(player_s.p_time_raw))/3600

if player_s.delta == 0: #If this is the first access of the game, then delta_t == 0
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
    print player_g.f_j
    print ("___________________\n"
           "Welcome back to the game!\n"
           "Your very first login time: %s\n"
           "Hours since last login: %s\n\n"
           "Blocks of fishing juice you've acquired since the last login: %s\n\n"
           "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n"
           "Get out and do something useful in the meantime!\n"
           "Summoner's war DOES NOT COUNT.\n\n" %(f_time, h_s_l_login, int(h_s_l_login)))
    player_g.fish_away()
##    inv_display()
##    display_menu()
else:
    print "Error."


##def delta_login(): #works correctly - Calculates the difference in seconds between now and the last login
##    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
##        reader = csv.reader(csv_file)#
##        stats = dict(reader)#
##        delta_t = int(round(float(stats["Create Time"]))) - int(round(float(stats["Last Login"]))) ##The initial create time and last login time aren't exactly the same!! That's why I need to round.
##        
##def first_time(): #works correctly - Prints the initial login time (creation of account time)
##    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
##        reader = csv.reader(csv_file)#
##        stats = dict(reader)#
##        f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(stats["Create Time"])))
##
##def previous_time(): #works correctly - Prints the last login time (most recent login time)
##    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
##        reader = csv.reader(csv_file)#
##        stats = dict(reader)#
##        p_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(stats["Last Login"])))
##
##def update_previous_time():
##    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
##        reader = csv.reader(csv_file)#
##        stats = dict(reader)#
##        stats["Last Login"] = time.time()
##    with open(uname+'.csv', 'wb') as csv_file: ## Change test to uname+
##        writer = csv.writer(csv_file, dialect = 'excel') 
##        for key, value in stats.items():
##            writer.writerow([key, value])
##
##def time_since_last_login():
##    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
##        reader = csv.reader(csv_file)#
##        stats = dict(reader)#
##        h_s_l_login = (float(time.time()) - float(stats["Last Login"]))/3600
##

##        


##   
##delta_login()
##first_time()
##previous_time()
##time_since_last_login()
##if delta_t == 0: #If this is the first access of the game, then delta_t == 0
##    new_acc_inv()
##    print ("Welcome to the game!\n"
##           "Your very first login time: %s\n"
##           "Hours since last login: %s\n" %(f_time, h_s_l_login))
##    inv_display()
##    update_previous_time()
##    display_menu()
##    
##elif delta_t < 0: #If this is NOT the first access, then delta_t will not == 0 (we will have overwritten the current login time to be different from the initial time) - TBC
##    update_previous_time()
##    print ("___________________\n"
##           "Welcome back to the game!\n"
##           "Your very first login time: %s\n"
##           "Hours since last login: %s\n\n"
##           "Blocks of fishing juice you've acquired since the last login: %s\n\n"
##           "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n"
##           "Get out and do something useful in the meantime!\n"
##           "Summoner's war DOES NOT COUNT.\n\n" %(f_time, h_s_l_login, int(h_s_l_login)))
##    inv_display()
##    display_menu()
##else:
##    print "Error."
##    

    
#print 'gamecode finish'
#print rand(1,10) - testing with/as syntax and RNG  uname+'
