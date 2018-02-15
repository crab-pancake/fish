import csv

class myClass(object):
    def __init__(self):
        self.file = dict(csv.reader(open('test.csv', 'r')))
    # def load(self):
    #     self.a = int(self.file["f_j"])
    #     self.b = int(self.file["mackerel"])
    #     self.c = int(self.file["cockle"])
    #     self.d = int(self.file["s_karp"])
    # def display(self): 
    #     print ("A: {}\nB: {}\nC: {} \nD: {}".format(self.a, self.b, self.c, self.d))
    def show(self):
        for key in self.file:
            print("showprint: %s: %s" % (key, self.file[key]))
    def kwargtest(self,**kwargs):
        kwargs = self.file
        for key in kwargs:
            print("methodprint: %s: %s" % (key, kwargs[key]))


test = myClass()
# test.display()
# test.load()
# for line in test.file:
#     print('line:',line)
# test.display()

test.kwargtest() #both these work
test.show()      #perfectly