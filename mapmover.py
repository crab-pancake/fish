import csv
import json
import universals as univ

class Location(object):
    def __init__(self, code, name, description, travel):
        self.code = code
        self.name = name
        self.description = description
        self.content = {}
        with open('./locations/'+self.code+'_l.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['type'] == 'shop':
                    self.content[row['code']] = Shop(row['code'],row['name'],row['desc'],row['introline'],row['exitline'])
                elif row['type'] == 'FishSpot':
                    self.content[row['code']] = FishSpot(row['code'],row['name'],row['desc'],row['min_level'])
        self.destinations = travel.split(';')
    def displaycontent(self):
        for num, place in enumerate(self.content):
            print(num+1, self.content[place].name)
        while True:

            decision = int(input("Where do you want to go?"))

        

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
                    print(univ.error(0))
            except ValueError:
                print(univ.error(1))
    def sell(self):
        player.disp_currency('00001')
    def buy(self):
        player.disp_currency('00001')

class FishSpot(Place):
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

    class Player(object):
        def __init__(self):
            self.inventory = {'i00000': 10, 'i00001': 20, 'i01001': 5, 'i01003': 13, 'i01006': 3, 'i02002': 5}
            self.position = "000"
        def disp_currency(self, currency):
            print("You now have %s %s." % (self.inventory[currency],univ.ListOfItems[currency].description))
        def travel(self):
            self.traveller = []
            for number, value in enumerate(places[self.position].destinations):
                self.traveller.append(value)
                print(str(number + 1)+'.', places[value].name)
            while True:
                try:
                    self.destination = int(input('Type the number of the destination you want to travel to.\n>> '))-1
                    if 0<=self.destination<len(self.traveller):
                        self.position = places[self.position].destinations[self.destination]
                        print('You have moved to %s.'%(places[self.position].name))
                        print(places[self.position].description)
                        # print(places[self.position].content)
                        places[self.position].displaycontent()
                        break
                    else:
                        print('out of range')
                except ValueError:
                    print('nope')

    player = Player()
    player.travel()
    player.travel()

# chicken = "print('hello chicken')"
# exec(chicken) #nice, this works