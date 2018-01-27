import os

droptable = 'droptableTest'

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = 'tables/' + droptable + '.csv'
filepath = os.path.join(script_dir, rel_path)

'''
class Table:
  def __init__(self, realpart, imagpart):
  self.r = realpart
  self.i = imagpart
'''

with open(filepath, 'wb') as loottable:
  reader = csv.reader(loottable)
  lootsdict = dict(reader)
  nonlocal max_level = lootsdict["maxlevel"]

print max_level
