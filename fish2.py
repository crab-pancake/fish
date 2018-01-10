import time

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

def log_in():
  uname = raw_input("Enter your account name to login.\n>> ")
  print 'Logging in to account %s...' % (uname)
  try:
    acct = open(uname+'.txt', 'r+b')
    pw = acct.readlines()[2][3:]
    print pw
    pword = raw_input("Please type your password.\n>> ")
    if pw == pword:
      print 'Successfully logged in to account %s.' % (uname)
      execfile('gamecode.py')
    else:
      print 'Sorry, the username and password didn\'t match.'
      acct_ask()
    acct.close()
  except IOError:
    print 'Account by the name of %s doesn\'t exist.' % (uname)
    acct_ask()

def new_acct():
  uname = raw_input("Create an account: select your username.\n>> ")
  try:
    acct = open(uname+'.txt', 'r+b')
    print 'Account already exists.'
    acct.close()
    acct_ask()
  except IOError:
    print 'Creating account with username %s...' % (uname)
    acct = open(uname+'.txt', 'w+b')
    #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    acct.write(str(time.time()) + ' create time\n')
    acct.write(str(time.time()) + ' last login\n')
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
          acct.write('pw: '+pw+'\n')
          print 'Password confirmed, please log in to your account.'
          log_in()
          break
        else:
          print 'Sorry, the passwords didn\'t match.'
    acct.close()

acct_ask()

