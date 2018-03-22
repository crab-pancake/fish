import json
import csv
import universals as univ
import hashlib

def prettyprint(filename):
    with open(filename+'.json', 'r') as file:
        parsed = json.load(file)
        print(json.dumps(parsed, indent=4, separators=(',', ': ')))

def prettysave(filename):
    with open(filename+'.json', 'r') as file:
        parsed = json.load(file)
    with open(filename+'.json', 'w') as file:
        json.dump(parsed, file, indent=2, separators=(',', ': '))
    print('Saved prettily')
    
def update(username):
    try:
        with open('./PlayerAccts/%s_p.json'%(username), 'r') as file:
            reader = json.load(file)
            try:
                reader['createtime']=int(reader['create time'])
                reader['lastlogin']=int(reader['last login'])
            except KeyError:
                reader['createtime']=int(reader['createtime'])
                reader['lastlogin']=int(reader['lastlogin'])
            try:
                if not reader['equipment']:
                    reader['equipment']=dict.fromkeys(range(1,10),None)
            except KeyError:
                reader['equipment']=dict.fromkeys(range(1,10),None)
            player = univ.Player(**reader)
            newdict = {}
            for key in player.inventory:
                if key[0] == 'i':
                    newdict[key]=player.inventory[key]
                else:
                    newdict['i'+key]=player.inventory[key]
            for item in univ.ListOfItems.keys():
                newdict[item]=player.inventory.get(item,0)
            player.inventory=newdict
            for skill in univ.skills:
                player.exp[skill] = player.exp.get(skill, 0)
            if len(player.password)!=64:
                player.password=hashlib.sha256(player.password.encode('utf-8')).hexdigest()
            if len(player.position)!=3:
                player.position='000'
            player.save()
        print("Account updated.")
    except FileNotFoundError as e:
        raise e
t='test_acct'