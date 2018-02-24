import random
import time
import csv
from pathlib import Path

def acct_ask(): #This is complete
  while True:
    exist = input("Do you already have an account? (Y/N)\n>>" ).strip().lower()
    if exist=='y' or exist=='ye'or exist=='yes' or exist=='1':
      log_in()
      break
    elif exist=='n' or exist=='no' or exist=='0':
      new_acct()
      break
    else:
      print ('Invalid response, please try again.\n')

def new_acct():
  uname = input("Select new username:\n>> ").strip()
  try:
    with open(uname+'_i.csv', 'x', newline = '') as playerfile:
      print ('Creating account with username %s...' % (uname))
      writer = csv.writer(playerfile, dialect='excel')
      writer.writerow(['Create Time', time.time()])
      writer.writerow(['Last Login',0]) #changed lastlogin to set to 0 when acct is created
      writer.writerow(['exp',0])
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
            writer.writerow(['Password',pw]) #change this to write hash of password: import hashlib, find out how this works
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
  acc_path = Path("./%s_i.csv" % (uname))  #put this into lower line?
  if acc_path.is_file():
    with open(uname+'_i.csv', 'r') as file:
      playerfile = dict(csv.reader(file))
      pw = input("Please type your password.\n>> ")
      if pw == playerfile['Password']:
        print ('Successfully logged in to account %s.' % (uname))
        print('done')
        import gamecode
        gamecode.rungame(uname)
      else:
        print ('Sorry, the username and password didn\'t match.')
        acct_ask()
  else:
    print ('Account by the name of %s doesn\'t exist.' % (uname))
    acct_ask()

acct_ask()