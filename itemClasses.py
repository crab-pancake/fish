class Item(object):
    """items"""
    def __init__(self,code,name,desc,exp,baseRegen,acceptP,vendP,**kwargs):
        self.code=code
        self.name=name
        self.desc=desc
        self.exp=int(exp)
        self.baseRegen=float(baseRegen)
        self.acceptP=int(acceptP) # shop buys from player
        self.vendP=int(vendP) # shop sells to player
        self.type='other'
    def __str__(self):
        return "Item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Item(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass

class Fish(Item):
    def __init__(self,code,name,desc,exp,baseRegen,acceptP,vendP,minlvl,**kwargs):
        super().__init__(code,name,desc,exp,baseRegen,acceptP,vendP,**kwargs)
        self.type='fish'
        self.minlvl=int(minlvl)
    def __str__(self):
        return "Fish item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Fish(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

class Bait(Item):
    def __init__(self,code,name,desc,exp,baseRegen,acceptP,vendP,**kwargs):
        super().__init__(code,name,desc,exp,baseRegen,acceptP,vendP)
        self.type = 'bait'
    def __str__(self):
        return "Bait item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Bait(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

class Material(Item):
    def __init__(self,code,name,desc,exp,baseRegen,acceptP,vendP,**kwargs):
        super().__init__(code,name,desc,exp,baseRegen,acceptP,vendP,**kwargs)
        self.type='material'
    def __str__(self):
        return "Material item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Material(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)

class Equipment(Item):
    def __init__(self,code,name,desc,exp,baseRegen,acceptP,vendP,slot,equip,**kwargs):
        super().__init__(code,name,desc,exp,baseRegen,acceptP,vendP,**kwargs)
        self.type='equipment'
        self.slot=slot
        self.equipeffects=equip
    def __str__(self):
        return "Equipment item with code %s, name %s" % (self.code, self.name)
    def __repr__(self):
        return "Equipment(%r, %r, %r, %r)" % (self.code, self.name, self.desc, self.exp)