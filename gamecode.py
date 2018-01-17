from random import randint as rand
import csv
import time

##print 'gamecode'
##print uname
##print 'Your last login was '
##print 'gamecode finish'

def new_acc_inv(): #works correctly - Creates a new blank inventory and writes it to the player's secondary save file.
    inv = {"mackerel": 0, "cockle": 0, "s_karp": 0}
    with open('test.csv', 'wb') as playerfile: ## Change test to uname+
        writer = csv.writer(playerfile, dialect = 'excel')
        for key, value in inv.items():
            writer.writerow([key, value])

def delta_login(): #works correctly - Calculates the difference in seconds between now and the first login
    global delta_t
    with open('test1.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        delta_t = int(stats["first_time"]) - int(stats["current_time"]) ##'stats' is short for status

def first_time(): #works correctly - Prints the initial login time (creation of account time)
    global f_time
    with open('test1.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(stats["first_time"])))

def current_time(): #works correctly - Prints the last login time (most recent login time)
    with open('test1.csv', 'rb') as csv_file:#replace test1.csv
        reader = csv.reader(csv_file)#
        stats = dict(reader)#
        c_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(stats["current_time"])))
        
def inv_display(): #works correctly (for the basic inventory list currently)
    with open('test.csv', 'rb') as csv_file:#replace test.csv
        reader = csv.reader(csv_file)
        inv = dict(reader)
        print ("YOUR INVENTORY:\n"
               "-------------------------\n"
               "Mackerel: {}\nCockles: {} \nShiny Magikarp: {}".format(inv["mackerel"], inv["cockle"], inv["s_karp"]))
   
delta_login()
if delta_t == 0: #If this is the first access of the game, then delta_t == 0
    new_acc_inv()
    first_time()
    print ("Welcome to the game!\n"
           "Your initial login time: %s" %(f_time))
    inv_display()
    
else: #If this is NOT the first access, then delta_t will not == 0 (we will have overwritten the current login time to be different from the initial time) - TBC
    print "Not a new login."
    

    

#print rand(1,10) - testing with/as syntax and RNG  uname+'
