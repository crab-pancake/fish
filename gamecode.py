from random import randint as rand
import csv
import time

##print 'gamecode'
##print uname
##print 'Your last login was '

#def mobilise_dict():
    

def new_acc_inv(): #works correctly - Creates a new blank inventory and writes it to the player's secondary save file.
    inv = {"mackerel": 0, "cockle": 0, "s_karp": 0}
    with open(uname+'_g_info.csv', 'wb') as playerfile: ## Change test to uname+
        writer = csv.writer(playerfile, dialect = 'excel')
        for key, value in inv.items():
            writer.writerow([key, value])

def delta_login(): #works correctly - Calculates the difference in seconds between now and the last login
    global delta_t
    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        delta_t = int(round(float(stats["Create Time"]))) - int(round(float(stats["Last Login"]))) ##The initial create time and last login time aren't exactly the same!! That's why I need to round.
        
def first_time(): #works correctly - Prints the initial login time (creation of account time)
    global f_time
    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(stats["Create Time"])))

def previous_time(): #works correctly - Prints the last login time (most recent login time)
    global p_time
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
    global h_s_l_login
    with open(uname+'.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        h_s_l_login = (float(time.time()) - float(stats["Last Login"]))/3600
        
def inv_display(): #works correctly (for the basic inventory list currently)
    with open(uname+'_g_info.csv', 'rb') as csv_file:#replace test.csv
        reader = csv.reader(csv_file)
        inv = dict(reader)
        print ("YOUR INVENTORY:\n"
               "-------------------------\n"
               "Mackerel: {}\nCockles: {} \nShiny Magikarp: {}".format(inv["mackerel"], inv["cockle"], inv["s_karp"]))
   
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
elif delta_t < 0: #If this is NOT the first access, then delta_t will not == 0 (we will have overwritten the current login time to be different from the initial time) - TBC
    update_previous_time()
    print ("___________________\n"
           "Welcome back to the game!\n"
           "Your very first login time: %s\n"
           "Hours since last login: %s\n\n"
           "Blocks of fishing juice you've acquired: %s\n\n"
           "HINT: you get 1 unit of juice per hour elapsed between the current and last logins.\n"
           "Get out and do something useful in the meantime!\n"
           "Summoner's war DOES NOT COUNT.\n\n" %(f_time, h_s_l_login, int(h_s_l_login)))
    inv_display()
else:
    print "Error."
    

    
#print 'gamecode finish'
#print rand(1,10) - testing with/as syntax and RNG  uname+'
