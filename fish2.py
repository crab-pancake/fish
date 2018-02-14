import random
import time
import csv

def acct_ask(): #This is complete
  while True:
    exist = input("Do you already have an account? (Y/N)\n>>" ).lower()
    if exist=='y' or exist=='ye'or exist=='yes' or exist=='1':
      log_in()
      break
    elif exist=='n' or exist=='no' or exist=='0':
      new_acct()
      break
    else:
      print ('Invalid response, please try again.\n')

def new_acct():
  uname = input("Select new username:\n>> ")
  try:
    with open(uname+'.csv', 'x', newline = '') as playerfile:#+'_g_info.csv'
      print ('Creating account with username %s...' % (uname))
      fieldnames = ['Create Time', 'Last Login', 'Password']
      writer = csv.writer(playerfile, dialect='excel')
      writer.writerow(['Create Time', str(time.time())])
      writer.writerow(['Last Login',0]) #changed lastlogin to set to 0 when acct is created
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
            writer.writerow(['Password',pw])
            print ('Password confirmed, please log in to your account.')
            playerfile.close() #closing first will write the stuff to the file before log_in is called, avoids indexerror
            log_in()
            break
          else:
            print ('Sorry, the passwords didn\'t match.')
  except FileExistsError:
    print ('Account already exists.')
    acct_ask()

def log_in():
  #global uname #what does this do?
  uname = input("Enter your account name to login.\n>> ")
  print ('Logging in to account %s...' % (uname))
  try:
    playerfile = open(uname+'.csv', 'r')
    playerfile.close()
    with open(uname+'.csv', 'r') as playerfile:
      reader = csv.reader(playerfile)
      stats = dict(reader)
      password=stats['Password']
      print ('Password:',password)
      pword = input("Please type your password.\n>> ")
      if password == pword:
        print ('Successfully logged in to account %s.' % (uname))
        exec(open('./gamecode.py').read())
      else:
        print ('Sorry, the username and password didn\'t match.')
        acct_ask()
  except IOError:
    print ('Account by the name of %s doesn\'t exist.' % (uname))
    acct_ask()

acct_ask()