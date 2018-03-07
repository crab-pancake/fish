import random as rand

def drop_item():
    rare_bound = 0.1
    var = rand.random()
    if var <= 0.1 *rare_bound:
	    print("Rare item!")
    elif var <= rare_bound:
        print("Uncommon item.")
    else:
        print(var)
        print("Common item.")


if __name__ == '__main__':
    drop_item()