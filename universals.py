import csv

class Item(object):
    """items"""
    def __init__(self, code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type):
        self.code = code
        self.item_name = item_name
        self.description = description
        self.exp = exp
        self.min_level = min_level
        self.sale_p = sale_p
        self.buy_p = buy_p
        self.h2 = h2
        self.h3 = h3
        self.i_type = i_type
        self.type = 'other'
    def __str__(self):
        return "Item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Item(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Fish(Item):
    def __init__(self, code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type):
        super().__init__(code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type)
        self.type = 'fish'
        self.sell_price = 5
    def __str__(self):
        return "Fish item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Fish(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Bait(Item):
    def __init__(self, code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type):
        super().__init__(code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type)
        self.type = 'bait'
    def __str__(self):
        return "Bait item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Bait(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

class Material(Item):
    def __init__(self, code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type):
        super().__init__(code, item_name, description, exp, min_level, sale_p, buy_p, h2, h3, i_type)
        self.type = 'material'
    def __str__(self):
        return "Material item with code %s, name %s" % (self.code, self.item_name)
    def __repr__(self):
        return "Material(self, %r, %r, %r, %r, %r)" % (self.code, self.item_name, self.description, self.exp, self.min_level)

ListOfItems = {}
with open('allitems_m.csv', 'r') as readfile:
    reader = csv.DictReader(readfile)
    for row in reader:
        if row['i_type'] == 'fish':
            ThisItem = Fish(row['code'], row['item_name'], row['description'], int(row['exp']), int(row['min_level']), int(row['sale_p']), int(row['buy_p']), row['h2'], row['h3'], row['i_type'])
            ListOfItems[ThisItem.code] = ThisItem
        elif row['i_type'] == 'bait':
            ThisItem = Bait(row['code'], row['item_name'], row['description'], int(row['exp']), int(row['min_level']), int(row['sale_p']), int(row['buy_p']), row['h2'], row['h3'], row['i_type'])
            ListOfItems[ThisItem.code] = ThisItem
        else:
            ThisItem = Item(row['code'], row['item_name'], row['description'], int(row['exp']), int(row['min_level']), int(row['sale_p']), int(row['buy_p']), row['h2'], row['h3'], row['i_type'])
        ListOfItems[ThisItem.code] = ThisItem

def error_message(number):
    print ("Error %s: That is invalid. Try again." % (number)) 