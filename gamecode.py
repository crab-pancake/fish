import random
import csv
import time

class User_s(object):
    """user stats file for times and such."""
    def __init__(self, f_time_raw, p_time_raw, pw, uname):
        self.f_time_raw = f_time_raw
        self.p_time_raw = p_time_raw
        self.pw = pw
        self.delta = float(p_time_raw) - float(f_time_raw)
        self.uname = uname
        self.f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(f_time_raw)))
        self.p_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(p_time_raw)))
        self.hsll = (time.time() - float(p_time_raw))/3600
    def update_time(self):
        self.p_time_raw = time.time()
    def save(self):
        stats = {"Create Time":self.f_time_raw, "Last Login": self.p_time_raw, "Password":self.pw}
        with open(self.uname+'_i.csv', 'w', newline='') as savefile:
            writer = csv.writer(savefile, dialect='excel')
            for key, value in stats.items():
                writer.writerow([key, value])

class User_g(object):
    """ A User's account. Defines the amount of fishing juice and starting items."""
    def __init__(self, uname):
        self.uname = uname
        self.inv = {}
        self.allitems = 0
        with open('allitems.csv', 'r') as allitems:
            self.allitems = dict(csv.reader(allitems))
        for key in self.allitems:
            self.inv[key] = 0      #creates a dictionary called inv and creates keys for all the entries from allitems, sets all quantities to 0
    def fish_away(self):
        with open('table.csv', 'r') as table: #table.csv will be changed to the player's specific level loottable
            self.table = dict(csv.reader(table))
            while True:
                fish = input("Would you like to fish? Press Y for yes, N for no.\n>> ").lower()
                if fish == "y":
                    if self.inv['f_j'] >0:
                        self.inv['f_j'] -= 1
                        rng = random.randint(1,100)
                        catch = False
                        for key in self.table:
                            if rng >= int(self.table[key]):
                                self.inv[key] =  int(self.inv[key]) +1
                                print("You caught a",key+'.')
                                print("You have",self.inv[key],key+'.') #how can I add a description? May have to move away from csv files or dictionaries
                                self.suc_fish()
                                catch = True
                                break
                        if catch == False:
                            print("You didn't catch anything.")
                            self.suc_fish()
                    else:
                        print ("You have no units of fishing juice left. Try waiting at least another hour.")
                elif fish == "n":
                    break
                else:
                    print ("Invalid response, try again.\n")
    def suc_fish(self):
        print ("You have",self.inv['f_j'],"fishing juice remaining.")
        self.save()
    def save(self):   #done
        with open(self.uname+'_g_info.csv', 'w', newline='') as savefile:
            writer = csv.writer(savefile, dialect = 'excel')
            for key, value in self.inv.items():
                writer.writerow([key, value])

    def load(self):   #done
        with open(self.uname+'_g_info.csv', 'r') as loadfile:
            loader = dict(csv.reader(loadfile))
            for key in loader:
                self.inv[key] = loader[key]

    def shop_display(self):
        print("Coles")
    def help_display(self):
        print("\nHELP\n"
            "\n----------------------------\n"
            "\nHistory:\nJerry and Dayu thought of this game as they were walking with Evan and Mummy, along Lake Nordonskjold, W-Trek, Patagonia, Chile in late December 2017. The inspiration came from many hours of idle chat, but at least it encouraged them to do somethiing productive!\n"
            "\nAim:\nThis is a time based game, where you as the player character gather 'fishing juice' to catch fish, upgrade your setup and further your fishing capabilities.\n"
            "\nInitial setup:\nYou'll begin with 10 fishing juice and no fish. Under the 'Menu' option, choose 'Fish!' to use up your fishing juice and catch fish. Each time you'll have a go at fishing and deplete your fishing juice by one. You'll gather more fishing juice by logging off (1 per hour is the base rate) and relogging on.\n"
            "\nBuying and selling:\n Enter the corresponding number 'Visit shop' in order to buy and sell your fish to gain gold. Use your gold to upgrade your fishing set up. For example, the cheapest upgrade will is the 'Reinforced net', which will increase your fishing juice gathering rate by 10%.\n"
            "\nFinal words:\n Good luck! We'll be slowly adding in extra features, but be patient as we are new :3")
    def display_menu(self):
    	while True:
            menu = input("\nMENU\n"
                    "----------------------------\n"
                    "1. Display inventory\n"
                    "2. Fish!\n"
                    "3. Visit shop (sell and buy items)\n"
                    "4. Help\n"
                    "5. Exit game\n> ")
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
        print("YOUR INVENTORY:\n-------------------------")
        for key in self.inv:
            print('%s: %s' % (key, self.inv[key]))

player_s = User_s(stats["Create Time"], stats["Last Login"], stats["Password"], uname)

if player_s.p_time_raw == '0': #If this is the first access of the game, then ptimeraw == 0
    print('running first mode') #for debug purposes
    player_s.update_time()
    player_s.save()
    player_g = User_g(uname)
    player_g.inv['f_j'] = 10
    print ("Welcome to the game! This is your first login. \n"
           "Account creation time: %s"%(player_s.f_time))
    player_g.display_menu()

elif player_s.delta > 0: 
    print('running second mode') #for debug purposes
    player_g = User_g(uname)
    player_s.update_time()
    player_s.save()
    player_g.load()
    player_g.inv['f_j']=int(player_g.inv['f_j'])+int(player_s.hsll)
    print ("___________________\n"
           "Welcome back to the game!\n"
           "Account creation time: %s\n"
           "Time since last login: %s hrs, %s mins\n\n"
           "You've acquired [ %s ] Blocks of fishing juice since the last login. \n\n"   
           "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n" 
           %(player_s.f_time, int(player_s.hsll), int((player_s.hsll-int(player_s.hsll))*60), int(player_s.hsll)))
    player_g.display_menu()

elif (player_s.delta < 0):
    print("Error happened.")
