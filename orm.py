import pymysql
import re
import inspect
class sql(object):
    def __init__(self,name='test',table_name='sqltest',host='localhost',user='root',password='123456'):
        self.name = name
        self.table_name = table_name
        self.con = pymysql.connect(host=host,user=user,password=password,database=self.name)
        self.cursor = self.con.cursor()

    def insert(self,**kwargs):
        #cursor = self.cursor
        condition = ''
        for key in kwargs:
            condition += str(kwargs[key])+','
        condition = condition.rstrip(',')
        sql = "INSERT INTO "+self.table_name+" VALUES ("+condition+");"
        try:
            # 尝试
            self.cursor.execute(sql)
            self.con.commit()
        except:
            # 发出错误
            raise Exception

    def update(self,*args,**kwargs):
        condition = ''
        for i in args:
            condition += i+','
        condition = condition.rstrip(',')
        data = ''
        for key in kwargs:
            data += str(key)+'='+str(kwargs[key])+','
        data = data.rstrip(',')
        sql = "UPDATE "+self.table_name+" SET "+data+" WHERE "+condition+";"
        print(sql)
        self.cursor.execute(sql)
        self.con.commit()

    def search(self,*args):
        condition = ''
        for i in args:
            condition += i+','
        condition = condition.rstrip(',')
        sql = 'SELECT * FROM '+self.table_name+' WHERE ('+condition+');'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def delete(self,*args):
        condition = ''
        for i in args:
            condition += i+','
        condition = condition.rstrip(',')
        sql = 'DELETE FROM '+self.table_name+' WHERE ('+condition+');'
        self.cursor.execute(sql)
        self.con.commit()

    def close(self):
        self.cursor.close()
        self.con.close()



class Field(object):
    def isNum(self,value):
        try:
            value + 1
        except TypeError:
            return False
        else:
            return True

    def __init__(self,name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other,str):
            return str(self.name)+'=\''+str(other)+'\''
        else:
            if other == None:
                return str(self.name)+'='+str('null')
            return str(self.name)+'='+str(other)

    def __lt__(self, other):
        if self.isNum(other):
            return str(self.name)+'<'+str(other)
        else:
            raise TypeError

    def __gt__(self, other):
        if self.isNum(other):
            return str(self.name)+'>'+str(other)
        else:
            raise TypeError

    def __le__(self,other):
        if self.isNum(other):
            return str(self.name)+'<='+str(other)
        else:
            raise TypeError

    def __ge__(self,other):
        if self.isNum(other):
            return str(self.name)+'>='+str(other)
        else:
            raise TypeError

    def __ne__(self, other):
        if isinstance(other,str):
            return str(self.name)+'!=\''+str(other)+'\''
        else:
            if other == None:
                return str(self.name)+'='+str('null')
            return str(self.name)+'!='+str(other)



if __name__ == '__main__':
    db = sql()
    id = Field('id')
    sex = Field('sex')
    #db.insert(id=1,sex='\'girl\'')
    #db.delete(id==1)
    #db.update(id==1,id=2,sex='\'boy\'')
    #db.close()
    # print(varname(name1))
    # a.search(name<123,name>120)


