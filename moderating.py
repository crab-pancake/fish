import json
import csv
import universals as univ
import hashlib

def prettyprint(filename):
    with open('./PlayerAccts/'+filename+'_p.json', 'r') as file:
        parsed = json.load(file)
        print(json.dumps(parsed, indent=4, separators=(',', ': ')))

def prettysave(filename):
    with open('./PlayerAccts/'+filename+'_p.json', 'r') as file:
        playerfile = json.load(file)
    with open('./PlayerAccts/'+filename+'_p.json', 'w') as file:
        json.dump(playerfile, file, indent=2, separators=(',', ': '))

def update(username):
    with open('./PlayerAccts/%s_p.json'%(username), 'r') as file:
        rdr = json.load(file)
        try:
            rdr['createtime']=int(rdr['create time'])
            rdr['lastlogin']=int(rdr['last login'])
        except KeyError:
            rdr['createtime']=int(rdr['createtime'])
            rdr['lastlogin']=int(rdr['lastlogin'])
        if len(rdr['password'])!=64:
            rdr['password']=hashlib.sha256(rdr['password'].encode('utf-8')).hexdigest()
        try:
            rdr['equipment']
        except KeyError:
            rdr['equipment']={}
        player = univ.Player(rdr['username'],rdr['password'],rdr['createtime'],rdr['lastlogin'],rdr['exp'],rdr['inventory'],rdr['position'],rdr['equipment'])
        newdict = {}
        for key in player.inventory:
            if key[0] == 'i':
                newdict[key]=player.inventory[key]
            else:
                newdict['i'+key]=player.inventory[key]
        player.inventory=newdict
        for skill in univ.skills:
            player.exp[skill] = player.exp.get(skill, 0)
        if len(player.position)!=3:
            player.position='000'
        player.save()
    print("Account updated.")

if __name__ == "__main__":
    while True:
        exec(input(">>> "))