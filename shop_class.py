class Shop(object):
    def __init__(self, code, name, desc, buy_stock, sell_stock, introline, exitline):
        self.code = code
        self.name = name
        self.desc = desc
        self.buy_stock = buy_stock.split(';')
        self.sell_stock = sell_stock.split(';')
        self.introline = introline
        self.exitline = exitline
        # with open('./locations/003_l.csv', 'r') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         self.shop_example[row['code']] = Shop(row['code'],row['name'],row['desc'],row['buy_stock'],row['sell_stock'],row['introline'],row['exitline'])
    def shop_display(self):
        while True:
            shop = input(self.introline)
            if shop == 'b':
                self.shop_buy()
            elif shop == 's':
                self.shop_sell()
            elif shop == 'x':
                break
            else:
                self.error_message(0)
    def error_message(self):
        print("Error occurred.")
    def disp_currency(self,currency):
        print("You have %s gold." % player.inventory[currency])
    def shop_buy(self):
        print("The following items are available for purchase:")
        for i in self.sell_stock:
            print("%s: %s" %(univ.ListOfItems[i].description,univ.ListOfItems[i].buy_p))
        while True:
            purchase = input("What items would you like to purchase? {Type the exact name of the item you wish to purchase. Or press x to return.}\n>> ")
            if purchase == 'x':
                 break
            itemfound = False
            for key in self.sell_stock:
                if univ.ListOfItems[key].description.lower() == purchase:
                    itemfound = True
                    buyitem = univ.ListOfItems[key]
                    while True:
                        purchase_q = input("How many [%s] would you like to purchase? Purchase price: [%s]. Or press 'x' to cancel.\n>> " % (buyitem.description, buyitem.buy_p))
                        if purchase_q == 'x':
                            break
                        try:
                            quantity = int(purchase_q)
                            if 0 < int(player.inventory['i00001']) < quantity*int(buyitem.buy_p):
                                self.error_message()
                            else:
                                player.inventory[key] += quantity
                                player.inventory['i00001'] -= quantity*int(buyitem.buy_p)
                                print("You now have %s %s." % (player.inventory[key],buyitem.description))
                                self.disp_currency('i00001')
                                # player.save()
                                break
                        except ValueError:
                            self.error_message
            if itemfound == False:
                print("No items found.")
    def shop_sell(self):#shop_s_code - this can be used to define a type of shop. e.g. '01' - corresponds to a fishing shop, where you can sell all your fish.
        while True:
            print("\nThis shop will purchase the following items from you:\n")
            for key in self.buy_stock:
                sell_fish = ("%s :%s    Sale price:%s" % (univ.ListOfItems[key].description, player.inventory[key], univ.ListOfItems[key].sale_p))
                print(sell_fish)

            sale = input("Type in the EXACT name of the item you wish to sell. Or type x to return.\n>> ").lower()
            if sale == 'x':
                break
            for key in self.buy_stock:
                if univ.ListOfItems[key].description.lower() == sale:
                    while True:
                        try:                    
                            sale_q = int(input("How many [%s] would like you to sell? Maximum number to sell: [%s] Sale price: [%s]\n>> " % (univ.ListOfItems[key].description, player.inventory[key], univ.ListOfItems[key].sale_p)))
                            if sale_q > player.inventory[key] or 0 > sale_q:
                                self.error_message
                            else:
                                player.inventory[key] -= sale_q
                                player.inventory['i00001'] += sale_q*int(univ.ListOfItems[key].sale_p)
                                print("You now have %s %s." % (player.inventory[key],univ.ListOfItems[key].description))
                                self.disp_currency('i00001')
                                # self.save()
                                break
                        except ValueError:
                            self.error_message()


if __name__ == "__main__":
    import csv
    import universals as univ

    class Player(object):
        def __init__(self):
            self.inventory = {'i00000': 10, 'i00001': 1000, 'i01001': 5, 'i01002': 5,'i01003': 13, 'i01004': 5,'i01005': 100,'i01006': 3, 'i02001':0, 'i02002': 5}


    player = Player()

   
    shop_example = {}

    with open('./locations/003_l.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            shop_example[row['code']] = Shop(row['code'],row['name'],row['desc'],row['buy_stock'],row['sell_stock'],row['introline'],row['exitline'])
    # print(shop_example['l0021'].desc) #This works
    shop_example['l0021'].shop_display()