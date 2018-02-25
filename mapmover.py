import csv

class Location(object):
    def __init__(self, code, name, desc, travel):
        self.code = code
        self.name = name
        self.desc = desc
        self.content = {}
        with open('000_l.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.content[row['code']] = Shop(row['code'],row['introline'],row['exitline'])
                break
        self.destinations = travel.split(';')
    def travel(self):
        print(self.destinations)
        for number, value in enumerate(self.destinations, 1):
            print(number, places[value].name)

class Place(object):
    def __init__(self):
        pass

class Shop(Place):
    """Class for shops selling different things."""
    def __init__(self, code, IntroLine, ExitLine):
        self.code = code
        self.intro = IntroLine
        self.exit = ExitLine
        # with open(code+'_s.csv', 'r') as file:
            # pass
    def shopfront(self):
        print(self.intro)
        while True:
            try:
                response = int(input("""What would you like to do?
                    1. Sell
                    2. Buy
                    3. Exit\n"""))
                if response == 1:
                    self.sell()
                elif response == 2:
                    self.buy()
                elif response == 3:
                    print(self.exit)
                    break
                else:
                    print(self.error(0))
            except ValueError:
                print(self.error(1))
    def sell(self):
        print("sell items here")
    def buy(self):
        print("buy items here")
    def error(self, number):
        return "Error %i. Please try again." % (number)

class FishingSpot(object):
    """Class for fishing spots."""
    def __init__(self, name, min_level, loottable, weather):
        self.name = name
        self.min_level = min_level
        self.loottable = loottable+'_t.csv'
        self.weather = weather
    def StartFishing(self):
        pass

if __name__ == "__main__":
    shoppe = Shop(1,'Hello there!','Goodbye!')
    shoppe.shopfront()
    places = {}
    # with open('locations_l.csv', 'r') as file:
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         place = Location(row['code'], row['name'], row['desc'], row['travel'])
    #         places[row['code']] = place
    # places['000'].travel()
    # print(places['000'].content['00001'].shopfront())

# chicken = "print('hello chicken')"
# exec(chicken) #nice, this works