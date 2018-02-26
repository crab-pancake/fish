import json
import csv


def prettyprint(filename):
    with open(filename+'_p.json', 'r') as file:
        parsed = json.load(file)
        print(json.dumps(parsed, indent=4, separators=(',', ': ')))

def prettysave(filename):
    with open(filename+'_p.json', 'r') as file:
        playerfile = json.load(file)
    with open(filename+'_p.json', 'w') as file:
        json.dump(playerfile, file, indent=2, separators=(',', ': '))

def convert(username):
    stats = {"username": username, 
        "password": "", 
        "createtime": 0,
        "lastlogin": 0,
        "exp": {"fishing":0},
        "inventory":{},
        "position": 'here'
        }
    inventory = {}
    with open(username+'_i.csv', 'r') as file:
        reader = dict(csv.reader(file))
        for row in reader:
            if row == "exp":
                fishexp = int(reader[row])
            else:
                try: 
                    num = float(reader[row])
                    stats["".join(row.split()).lower()]=num
                except ValueError:
                    stats["".join(row.split()).lower()]=reader[row]
    stats["exp"] = {"fishing": fishexp}
    with open(username+"_g.csv", 'r') as file:
        reader = dict(csv.reader(file))
        for row in reader:
            inventory[row] = int(reader[row])
    stats['inventory'] = inventory

    with open(username+'_p.json', 'w') as file:
        json.dump(stats, file)

if __name__ == "__main__":
    uname = input('type account name to convert & prettyprint\n>> ')
    convert(uname)
    prettyprint(uname)