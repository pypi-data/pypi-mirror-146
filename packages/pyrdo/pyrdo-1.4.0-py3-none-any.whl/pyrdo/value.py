def valueConverter(value,dataType):
    '''
    convert value into specific valuetype
    :param value: original value
    :param dataType: target dataType
    :return: return value after converting
    '''
    if dataType == 'int':
        value = int(value)
    if dataType == 'nvarchar':
        value = str(value)
    return(value)
def valueWrapper(value,valueType,auxKey):
    '''
    set the value into a object
    :param value: value
    :param valueType: valueType
    :param auxKey: aux key
    :return:
    '''
    if valueType == 'simple':
        res = value
    else:
        res = {}
        res[auxKey] = value
    return(res)
class Value():
    def __init__(self,value):
        self.value = value

    def convertor(self,dataType):
        self.dataType = dataType
        if self.dataType == 'int':
            res = int(self.value)
        if self.dataType == 'nvarchar':
            res = str(self.value)
        if self.dataType == 'varchar':
            res = str(self.value)
        return (res)
    def wrapper(self,valueType,auxKey):
        self.valueType = valueType
        self.auxKey = auxKey
        if self.valueType == 'simple':
            res = self.value
        else:
            res = {}
            res[self.auxKey] = self.value
        return (res)
if __name__ == '__main__':
    aa =Value(value='123')
    print(aa.convertor('int'))
    bb = Value(value='bb')
    cc =bb.wrapper(valueType='complex',auxKey='fname')
    print(cc)