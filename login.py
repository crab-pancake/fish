import random
import time
import csv
import json
from pathlib import Path
import universals as univ

def acct_ask(): #This is complete
    while True:
        exist = input("Do you already have an account? (Y/N)\n>>" ).strip().lower()
        if exist in univ.yes:
            log_in()
            break
        elif exist in univ.no:
            new_acct()
            break
        else:
            univ.error(0)

def new_acct():
    uname = input("Select new username:\n>> ").strip()
    try:
        with open('./PlayerAccts/'+uname+'_p.json', 'x') as playerfile:
            print ('Creating account with username %s...' % (uname))
            skills = ['fishing']
            exp = dict.fromkeys(skills,0)
            stats = {'username': uname, 'password':'','createtime':time.time(),'lastlogin':0,'exp':exp, 'inventory':{}, 'position':'000'} #set lastlogin to 0 on acct creation
            while True:
                pw = input("Enter a password longer than 3 characters, or type 'back' to cancel.\n>>")
                if pw.lower() == 'back':
                    acct_ask()
                    break
                elif len(pw) < 3:
                    print ('Please enter a password longer than 3 characters.')
                else:
                    pwconfirm = input("Confirm password.\n>>")
                    if pw == pwconfirm:
                        stats['password'] = pw #change this to write hash of password: import hashlib, find out how this works
                        json.dump(stats, playerfile)
                        print ('Password confirmed, please log in to your account.')
                        playerfile.close() #closing first will write the stuff to the file before log_in is called, avoids indexerror
                        log_in()
                        break
                    else:
                        print ("Sorry, the passwords didn't match.")
    except FileExistsError:
        print ('Account with the username %s already exists.' % (uname))
        acct_ask()

def log_in():
    uname = input("Enter your account name to login.\n>> ").strip()
    print ('Logging in to account %s...' % (uname))
    acc_path = Path("./PlayerAccts/%s_p.json" % (uname))  #put this into lower line?
    if acc_path.is_file():
        with open('./PlayerAccts/'+uname+'_p.json', 'r') as file:
            reader = json.load(file)
            pw = input("Please type your password.\n>> ")
            if pw == reader['password']:
                print ('Successfully logged in to account %s.' % (uname))
                file.close()
                import gamewrapper
                gamewrapper.start_acct(uname)
            else:
                print ('Sorry, the username and password didn\'t match.')
                acct_ask()
    else:
        print ('Account by the name of %s doesn\'t exist.' % (uname))
        acct_ask()

acct_ask()