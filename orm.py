import pymysql

class sql(object):
    def __init__(self,name):
        self.name = name
        self.table = table


    def connect(self,host,user,password):
        con = pymysql.connect(host=host,user=user,password=password,database=self.name)
        cursor = con.cursor()
        return cursor

    def insert(self,*args):
        pass

class test(object):
    def __init__(self,name):
        self.name = name
    def __eq__(self, other):
        return str(other)
        # print(self)
    def __lt__(self, other):
        return str(self.name)+'<'+str(other)

class test2(object):
    def search(self,*args):
        print(args)

if __name__ == '__main__':
    a = test2()
    b = test('name')
    a.search(b<123)


