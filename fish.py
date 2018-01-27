import random
import time
import csv

def acct_ask(): #This is complete
  while True:
    exist = raw_input("Do you already have an account? (Y/N)\n>>" ).lower()
    if exist=='y' or exist=='ye'or exist=='yes' or exist=='1':
      log_in()
      break
    elif exist=='n' or exist=='no' or exist=='0':
      new_acct()
      break
    else:
      print 'Invalid response, please try again.\n'

def new_acct():
  uname = raw_input("Select new username:\n>> ")
  try:
    playerfile = open(uname+'.csv', 'rb')
    print 'Account already exists.'
    playerfile.close()
    acct_ask()
  except IOError:
    print 'Creating account with username %s...' % (uname)
    with open(uname+'.csv', 'wb') as playerfile:
      writer = csv.writer(playerfile, dialect = 'excel')
      writer.writerow(['Create Time', time.time()])
      writer.writerow(['Last Login', time.time()])
      while True:
        pw = raw_input("Enter a password longer than 3 characters, or type 'back' to cancel.\n>>")
        if pw.lower() == 'back':
          acct_ask()
          break
        elif len(pw) < 3:
          print 'Please enter a password longer than 3 characters.'
        else:
          pwconfirm = raw_input("Confirm password.\n>>")
          if pw == pwconfirm:
            writer.writerow(['Password', pw])
            print 'Password confirmed, please log in to your account.'
            playerfile.close() #closing first will write the stuff to the file before log_in is called, avoids indexerror
            log_in()
            break
          else:
            print 'Sorry, the passwords didn\'t match.'

def log_in():
  global uname#
  uname = raw_input("Enter your account name to login.\n>> ")
  print 'Logging in to account %s...' % (uname)
  try:
    playerfile = open(uname+'.csv', 'rb')
    playerfile.close()
    with open(uname+'.csv', 'rb') as playerfile:
      reader = csv.reader(playerfile)
      stats = dict(reader)
      password=stats["Password"]#[row for i, row in enumerate(reader) if i == 2][0][1]
      print password
      pword = raw_input("Please type your password.\n>> ")
      if password == pword:
        print 'Successfully logged in to account %s.' % (uname)
        execfile('gamecode.py')
      else:
        print 'Sorry, the username and password didn\'t match.'
        acct_ask()
  except IOError:
    print 'Account by the name of %s doesn\'t exist.' % (uname)
    acct_ask()

acct_ask()

#with open('hello.csv', 'rb') as csvtest:
    #csvr = csv.reader(csvtest)
    #for row in csvr:
        #print row
