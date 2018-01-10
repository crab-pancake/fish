import csv
from pathlib2 import Path

"""
with open(uname+'.csv', 'wb') as player:
    writer = csv.writer(player, dialect = 'excel')
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

with open('csvtest.csv', 'rb') as csvtest:
    csvr = csv.reader(csvtest)
    for row in csvr:
        print row

with open('eggs.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, dialect = 'excel')
    print spamreader

"""

with open('qwer.csv') as fd:
    reader=csv.reader(fd)
    interestingrows=[row for idx, row in enumerate(reader) if idx in (0,2)]
    print interestingrows


#fyle = Path("asdflk.txt")
#print fyle.is_file()