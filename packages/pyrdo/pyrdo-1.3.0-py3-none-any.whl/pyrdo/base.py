class RdList:
    def __init__(self,data=[]):
        self.data = data
    def fromTuple(self,tuple):
        return(list(tuple))
    def toTuple(self):
        return tuple(self.data)
    def fromDictKeys(self,dict):
        self.dict = dict
        res = [i for i in self.dict.keys()]
        return res
    def fromDictValues(self,dict):
        self.dict = dict
        res = [i for i in self.dict.values()]
        return res
    def toDict(self,list_keys, list_values):
        '''
        transform the 2 lists into one dict
        :param list_keys: list keys
        :param list_values: list values
        :return: get a object with dict
        '''
        self.keys = list_keys
        self.values = list_values
        res = dict(zip(self.keys, self.values))
        return res
    def toDict2(self,Rdlist2):
        res = dict(zip(self.data, Rdlist2.data))
        return res
    def __add__(self, other):
        res = dict(zip(self.data, other.data))
        return res


class RdDict:
    def __init__(self,data):
        self.data = data
    def keysToList(self):
        res = [i for i in self.data.keys()]
        return res
    def valuesToList(self):
        res = [i for i in self.data.values()]
        return res
class RdTuple:
    def __init__(self,data=()):
        self.data = data
    def toList(self):
        return (list(self.data))
    def fromList(self,list1):
        return(tuple(list1))
if __name__ == '__main__':
    #方法1 列表转字典
    listA = ['A','B','C']
    listB =[1,2,3]
    l1 = RdList()
    mydata = l1.toDict(list_keys=listA,list_values=listB)
    print(mydata)


    # 方法2更高级的实现方式
    d1 = RdList(listA)
    d2  = RdList(listB)
    mydata2 = d1+d2
    print(mydata2)
    #元组转列表的列表的操作
    t1 = RdTuple(data=(1,2,3))
    print(t1.toList())
    a = [1,2,3]
    b = tuple(a)
    print(b)
    c = RdTuple()
    print(c.fromList(list1=a))
    #  处理数据
    dict1 = RdDict(mydata)
    key = dict1.keysToList()
    print(key)
    value = dict1.valuesToList()
    print(value)










