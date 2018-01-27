from random import randint as rand
import csv
import time

#def mobilise_dict():

h_s_l_login = 0 #hours since last login
delta_t = 0 #time between now and last login
f_time = 0 #time of first login
p_time = 0 #previous time
f_j = 0 #fishing juice
inv_ma = 0
inv_co = 0
inv_ka = 0
##
##def unwrap_inv():
##    with open(uname+'_g_info.csv', 'rb') as csv_file:
##        reader = csv.reader(csv_file)#
##        inv = dict(reader)#
##        print inv
##        f_j = inv["f_j"]
##        inv_ma = inv["mackerel"]
##        inv_co = inv["cockle"]
##        inv_ka = inv["s_karp"]
##    with open(uname+'.csv', 'rb') as csv_file:
##        reader = csv.reader(csv_file)#
##        stats = dict(reader)#
##        f_time = stats["Create Time"]
##        p_time = stats["Last Login"]
##    

def new_acc_inv(): #works correctly - Creates a new blank inventory and writes it to the player's secondary save file.
    inv = {"f_j":10, "mackerel": 0, "cockle": 0, "s_karp": 0}
    with open(uname+'_g_info.csv', 'wb') as playerfile: 
        writer = csv.writer(playerfile, dialect = 'excel')
        for key, value in inv.items():
            writer.writerow([key, value])

def delta_login(): #works correctly - Calculates the difference in seconds between now and the last login
    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        delta_t = int(round(float(stats["Create Time"]))) - int(round(float(stats["Last Login"]))) ##The initial create time and last login time aren't exactly the same!! That's why I need to round.
        
def first_time(): #works correctly - Prints the initial login time (creation of account time)
    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(stats["Create Time"])))

def previous_time(): #works correctly - Prints the last login time (most recent login time)
    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        p_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(stats["Last Login"])))

def update_previous_time():
    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        stats["Last Login"] = time.time()
    with open(uname+'.csv', 'wb') as csv_file: ## Change test to uname+
        writer = csv.writer(csv_file, dialect = 'excel') 
        for key, value in stats.items():
            writer.writerow([key, value])

def time_since_last_login():
    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        h_s_l_login = (float(time.time()) - float(stats["Last Login"]))/3600

def error_message():
    print "That's not a valid option. Try a different option, you nincompoop."
        
def inv_display(): #works correctly (for the basic inventory list currently)
    with open(uname+'_g_info.csv', 'rb') as csv_file:#replace test.csv
        reader = csv.reader(csv_file)
        inv = dict(reader)
        print ("YOUR INVENTORY:\n"
               "-------------------------\n"
               "Fishing juice: {}\nMackerel: {}\nCockles: {} \nShiny Magikarp: {}".format(inv["f_j"],inv["mackerel"], inv["cockle"], inv["s_karp"]))

##def fish_away():
##    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
##        reader = csv.reader(csv_file)#
##        stats = dict(reader)
##        print "Fishing juice: {}".format(inv["f_j")

def display_menu():
    menu_input = input ("\nMENU\n"
            "----------------------------\n"
            "1. Display inventory\n"
            "2. Fish!\n"
            "3. Visit shop (sell and buy items)\n"
            "4. Help\n"
            "5. Exit game\n")
    if menu_input == 1:
        inv_display()
##    if menu_input ==2:
##        fish_away
##    if menu_input == 3:
##        shop_display
##    if menu_input == 4:
##        help_display
##    if menu_input == 5:
##        break
    else:
        error_message()   
   
delta_login()
first_time()
previous_time()
time_since_last_login()
if delta_t == 0: #If this is the first access of the game, then delta_t == 0
    new_acc_inv()
    print ("Welcome to the game!\n"
           "Your very first login time: %s\n"
           "Hours since last login: %s\n" %(f_time, h_s_l_login))
    inv_display()
    update_previous_time()
    display_menu()
    
elif delta_t < 0: #If this is NOT the first access, then delta_t will not == 0 (we will have overwritten the current login time to be different from the initial time) - TBC
    update_previous_time()
    print ("___________________\n"
           "Welcome back to the game!\n"
           "Your very first login time: %s\n"
           "Hours since last login: %s\n\n"
           "Blocks of fishing juice you've acquired since the last login: %s\n\n"
           "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n"
           "Get out and do something useful in the meantime!\n"
           "Summoner's war DOES NOT COUNT.\n\n" %(f_time, h_s_l_login, int(h_s_l_login)))
    inv_display()
    display_menu()
else:
    print "Error."
    

    
#print 'gamecode finish'
#print rand(1,10) - testing with/as syntax and RNG  uname+'
