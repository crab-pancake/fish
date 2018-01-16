import pickle

example_dict= {"mackerel": 0, "cockle": 0, "s_karp": 0}

def catch_fish(z):
    while True:
        b = raw_input("Would you like to catch a fish?")
        if b == "1" or "y":
            example_dict["mackerel"] += 1
            print "You have", example_dict["mackerel"], "mackerel"
            pickle.dump(example_dict,open("save.p","wb"))

            b = pickle.load(open("save.p","rb"))
        else:
            print "Error."



catch_fish("")
