import csv
import json

class Location(object):
    def __init__(self, code, name, description, travel):
        self.code = code
        self.name = name
        self.description = description
        self.content = {}
        with open('./locations/'+self.code+'_l.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.content[row['code']] = Shop(row['code'],row['name'],row['desc'],row['introline'],row['exitline'])
        self.destinations = travel.split(';')
    def travel(self):
        return self.destinations
        for number, value in enumerate(self.destinations, 1):
            print(number, places[value].name)

class Place(object):
    def __init__(self, code, name, description):
        self.code = code
        self.name = name
        self.description = description

class Shop(Place):
    """Class for shops selling different things."""
    def __init__(self, code, name, description, IntroLine, ExitLine):
        super().__init__(code, name, description)
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
                    3. Exit\n>> """))
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

class FishingSpot(Place):
    """Class for fishing spots."""
    def __init__(self, code, name, description, min_level):
        super().__init__(code, name, description)
        self.min_level = min_level
        self.loottable = './tables/'+code+'_t.csv'
        # self.weather = weather  # add this later
    def StartFishing(self):
        with open(self.loottable, 'r') as file:
            reader = dict(csv.reader(file))

if __name__ == "__main__":
    places = {}
    with open('locations_l.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            place = Location(row['code'], row['name'], row['description'], row['travel'])
            places[row['code']] = place
    places['000'].travel()
    print(places['001'].content['l0011'].name)
    print(places['002'].description)
    print(places['002'].travel())
    # places['000'].content['l0001'].shopfront()

# chicken = "print('hello chicken')"
# exec(chicken) #nice, this works