from pyrda.dbms.rds import RdClient
from pyrdo.value import *
# function style:
def model_queryData(token="EDCFD199-AF57-4591-8BA9-CD44415B816B", FFormId='BD_MATERIAL', Ftype='head',
                    FEntityName='', FListCount=0, FActionName='Save'):
    app = RdClient(token=token)
    sql_head = "select FNodeName,FMainKey,FAuxKey,FDefaultValue,FDataType,FValueType  from t_api_erp_kdc"
    sql_where = "  where  Ftype ='" + Ftype + "'  and FEntityName ='" + FEntityName + "' and FIsShow =1  and FListCount = " + str(
        FListCount) + " and FFormId = '"
    sql_all = sql_head + sql_where + FFormId + "'  and FActionName ='" + FActionName + "'"
    # print(sql_all)
    data = app.select(sql=sql_all)
    return (data)
def model_queryMeta(token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL', FMainKey ='FIssueType',FActionName ='Save'):
    app = RdClient(token=token)
    sql_head = " select  FNodeName,FEntityName,FListCount,FMainKey,FAuxKey,Ftype,FDataType,FValueType from  t_api_erp_kdc  "
    sql_where = "  where   FIsShow =1  and FMainKey ='"+FMainKey+"' and FFormId = '"
    sql_all = sql_head + sql_where + FFormId + "'  and FActionName ='" + FActionName + "'"
    #print(sql_all)
    data = app.select(sql=sql_all)
    return(data)
def model_setValue(option,token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL', FMainKey ='FIssueType',FValue="",FActionName ='Save'):
    data = model_queryMeta(token=token,FFormId=FFormId,FMainKey=FMainKey,FActionName=FActionName)
    ncount = len(data)
    if ncount >0:
        for i in data:
            node_model = i['FNodeName']
            node_entity = i['FEntityName']
            node_count = i['FListCount'] - 1
            node_main = i['FMainKey']
            node_aux = i['FAuxKey']
            node_type = i['Ftype']
            node_datatype = i['FDataType']
            node_valueType = i['FValueType']
            if node_type == 'head':
                if node_valueType == 'simple':
                    option[node_model][node_main] = valueConverter(FValue, node_datatype)
                else:
                    # complex one
                    option[node_model][node_main][node_aux] = valueConverter(FValue, node_datatype)
            if node_type == 'entry':
                if node_valueType == 'simple':
                    option[node_model][node_entity][node_main] = valueConverter(FValue, node_datatype)
                else:
                    # complex one
                    option[node_model][node_entity][node_main][node_aux] = valueConverter(FValue, node_datatype)
            if node_type == 'entryList':
                if node_valueType == 'simple':
                    option[node_model][node_entity][node_count][node_main] = valueConverter(FValue, node_datatype)
                else:
                    # complex one
                    option[node_model][node_entity][node_count][node_main][node_aux] = valueConverter(FValue, node_datatype)
    return(option)
def model_BodySheet(token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',Ftype ='entry',FActionName ='Save'):
    app = RdClient(token=token)
    sql_head = "select  distinct FEntityName  from  t_api_erp_kdc"
    sql_where = "  where  Ftype ='"+Ftype+"'   and FFormId = '"
    sql_all = sql_head + sql_where + FFormId + "'  and FActionName ='" + FActionName + "'"
    # print(sql_all)
    data = app.select(sql=sql_all)
    return(data)
def model_tailCount(token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',Ftype ='entryList',FEntityName ='FEntityAuxPty',FActionName ='Save',):
    app = RdClient(token=token)
    sql_head = "  select distinct FListCount  from t_api_erp_kdc"
    sql_where = "  where  Ftype ='"+Ftype+"'  and FEntityName ='"+FEntityName+"'  and FIsShow =1  and FFormId = '"
    sql_all = sql_head + sql_where + FFormId + "'  and FActionName ='" + FActionName + "'"
    # print(sql_all)
    data = app.select(sql=sql_all)
    return(data)
def model_Item(node,i):
    '''

    :param node: means a head or a body row or  any one
    :param i: metadata each row
    :return:
    '''
    valueType = i['FValueType']
    dataType = i['FDataType']
    value = i['FDefaultValue']
    key = i['FMainKey']
    key2 = i['FAuxKey']
    value = valueConverter(value, dataType)
    node[key] = valueWrapper(value, valueType, key2)
    return(node)
def model_unity(data,option ,FEntityName ='',Ftype ='head'):
    '''
    model unity just used for head or entry with option as input
    :param data:
    :param option:
    :param FEntityName:
    :param Ftype:
    :return:
    '''
    ncount = len(data)
    # node represent a head or a body row
    node = {}
    if ncount >0:
        for i in data:
            node = model_Item(node,i)
        #是否为表头
        if Ftype =='head':
            option["Model"] = node
        else:
            option["Model"][FEntityName] = node
    else:
        pass
    return(option)
def model_unityNode(data,FEntityName ='',Ftype ='entryList'):
    '''
    model unityNode used for Entrylist without option as  input parameter
    :param data:
    :param FEntityName:
    :param Ftype:
    :return:
    '''
    ncount = len(data)
    # node represent a head or a body row
    node = {}
    if ncount >0:
        for i in data:
            node = model_Item(node,i)
    return(node)
def model_tailUnity(token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',Ftype='entryList',FEntityName ='FEntityAuxPty',FListCount=1,FActionName ='Save'):
    data = model_queryData(token=token, FFormId=FFormId, Ftype=Ftype,
                           FEntityName=FEntityName, FListCount=FListCount, FActionName=FActionName)
    res = model_unityNode(data, FEntityName=FEntityName, Ftype=Ftype)
    return(res)
def model_tail(option={},token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',Ftype='entryList',FEntityName ='FEntityAuxPty',FActionName ='Save'):
    data = model_tailCount(token=token,FFormId=FFormId,Ftype=Ftype,FEntityName=FEntityName,FActionName=FActionName)
    ncount = len(data)
    if ncount >0:
        #define the list
        res = []
        for i in data:
            # get the node for each list
            item = model_tailUnity(token=token,FFormId=FFormId,Ftype=Ftype,FEntityName=FEntityName,FListCount=i['FListCount'],FActionName=FActionName)
            res.append(item)
        option['Model'][FEntityName] = res
    return(option)
def model_head(token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',FActionName ='Save'):
    data = model_queryData(token=token,FFormId=FFormId,Ftype='head',FEntityName ='',FListCount=0,FActionName=FActionName)
    option = {}
    option = model_unity(data=data,option=option,FEntityName ='',Ftype='head')
    return(option)
def model_body(option,token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',FEntityName ='FSubHeadEntity',FActionName ='Save'):
    data = model_queryData(token=token,FFormId=FFormId,Ftype='entry',FEntityName =FEntityName,FListCount=0,FActionName=FActionName)
    ncount = len(data)
    option = model_unity(data=data,option=option,FEntityName = FEntityName,Ftype='entry')
    return(option)
def model_bodySet(option,token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',FActionName ='Save'):
    dataSheet = model_BodySheet(token=token, FFormId=FFormId, Ftype='entry', FActionName=FActionName)
    for sheet in dataSheet:
        option = model_body(option=option, token=token, FFormId=FFormId, FEntityName=sheet['FEntityName'],
                            FActionName=FActionName)
    return(option)
def model_tailSet(option,token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',FActionName ='Save'):
    tailSheet = model_BodySheet(token=token, FFormId=FFormId, Ftype='entryList', FActionName=FActionName)
    for i in tailSheet:
        option = model_tail(option=option, token=token, FFormId=FFormId, Ftype='entryList',
                            FEntityName=i['FEntityName'],
                            FActionName=FActionName)
    return(option)
def model_dataGen(token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId = 'BD_MATERIAL',FActionName ='Save'):
    #bill head
    option = model_head(token=token,FFormId=FFormId, FActionName=FActionName)
    #bill body
    option = model_bodySet(option=option,token=token,FFormId=FFormId,FActionName=FActionName)
    #tailList
    option = model_tailSet(option=option, token=token, FFormId=FFormId, FActionName=FActionName)
    return(option)
#object Style:
class Model():
    def __init__(self,token="EDCFD199-AF57-4591-8BA9-CD44415B816B",FFormId='BD_MATERIAL',FActionName='Save'):
        self.token = token
        self.FFormId = FFormId
        self.FActionName =FActionName
    def queryData(self, Ftype='head',FEntityName='', FListCount=0):
        self.Ftype = Ftype
        self.FEntityName = FEntityName
        self.FListCount = FListCount
        app = RdClient(token=self.token)
        sql_head = "select FNodeName,FMainKey,FAuxKey,FDefaultValue,FDataType,FValueType  from t_api_erp_kdc"
        sql_where = "  where  Ftype ='" + self.Ftype + "'  and FEntityName ='" + self.FEntityName + "' and FIsShow =1  and FListCount = " + str(
            self.FListCount) + " and FFormId = '"
        sql_all = sql_head + sql_where + self.FFormId + "'  and FActionName ='" + self.FActionName + "'"
        # print(sql_all)
        data = app.select(sql=sql_all)
        return (data)
    def queryMeta(self,FMainKey='FIssueType'):
        self.FMainKey = FMainKey
        app = RdClient(token=self.token)
        sql_head = " select  FNodeName,FEntityName,FListCount,FMainKey,FAuxKey,Ftype,FDataType,FValueType from  t_api_erp_kdc  "
        sql_where = "  where   FIsShow =1  and FMainKey ='" + self.FMainKey + "' and FFormId = '"
        sql_all = sql_head + sql_where + self.FFormId + "'  and FActionName ='" + self.FActionName + "'"
        # print(sql_all)
        data = app.select(sql=sql_all)
        return (data)
    def setValue(self,option,FMainKey='FIssueType', FValue=""):
        self.option = option
        self.FMainKey =FMainKey
        self.FValue = FValue
        data = self.queryMeta(FMainKey=self.FMainKey)
        ncount = len(data)
        if ncount > 0:
            for i in data:
                node_model = i['FNodeName']
                node_entity = i['FEntityName']
                node_count = i['FListCount'] - 1
                node_main = i['FMainKey']
                node_aux = i['FAuxKey']
                node_type = i['Ftype']
                node_datatype = i['FDataType']
                node_valueType = i['FValueType']
                if node_type == 'head':
                    if node_valueType == 'simple':
                        self.option[node_model][node_main] = valueConverter(FValue, node_datatype)
                    else:
                        # complex one
                        self.option[node_model][node_main][node_aux] = valueConverter(FValue, node_datatype)
                if node_type == 'entry':
                    if node_valueType == 'simple':
                        self.option[node_model][node_entity][node_main] = valueConverter(FValue, node_datatype)
                    else:
                        # complex one
                        self.option[node_model][node_entity][node_main][node_aux] = valueConverter(FValue, node_datatype)
                if node_type == 'entryList':
                    if node_valueType == 'simple':
                        self.option[node_model][node_entity][node_count][node_main] = valueConverter(FValue, node_datatype)
                    else:
                        # complex one
                        self.option[node_model][node_entity][node_count][node_main][node_aux] = valueConverter(FValue,
                                                                                                          node_datatype)
        return (self.option)

    def bodySheet(self,Ftype='entry'):
        self.Ftype = Ftype
        app = RdClient(token=self.token)
        sql_head = "select  distinct FEntityName  from  t_api_erp_kdc"
        sql_where = "  where  Ftype ='" + self.Ftype + "'   and FFormId = '"
        sql_all = sql_head + sql_where + self.FFormId + "'  and FActionName ='" + self.FActionName + "'"
        # print(sql_all)
        data = app.select(sql=sql_all)
        return (data)
    def queryEntity(self, Ftype='entry'):
        '''
        queryEntity is the alias name of bodySheet
        :param Ftype:
        :param FActionName:
        :return:
        '''
        self.Ftype = Ftype
        app = RdClient(token=self.token)
        sql_head = "select  distinct FEntityName  from  t_api_erp_kdc"
        sql_where = "  where  Ftype ='" + self.Ftype + "'   and FFormId = '"
        sql_all = sql_head + sql_where + self.FFormId + "'  and FActionName ='" + self.FActionName + "'"
        # print(sql_all)
        data = app.select(sql=sql_all)
        return (data)

    def tailCount(self, Ftype='entryList',FEntityName='FEntityAuxPty'):
        self.Ftype = Ftype
        self.FEntityName =FEntityName
        app = RdClient(token=self.token)
        sql_head = "  select distinct FListCount  from t_api_erp_kdc"
        sql_where = "  where  Ftype ='" + self.Ftype + "'  and FEntityName ='" + self.FEntityName + "'  and FIsShow =1  and FFormId = '"
        sql_all = sql_head + sql_where + self.FFormId + "'  and FActionName ='" + self.FActionName + "'"
        # print(sql_all)
        data = app.select(sql=sql_all)
        return (data)
    def item(self,node, i):
        self.node =node
        self.i = i
        valueType = self.i['FValueType']
        dataType = self.i['FDataType']
        value = self.i['FDefaultValue']
        key = self.i['FMainKey']
        key2 = self.i['FAuxKey']
        value = valueConverter(value, dataType)
        self.node[key] = valueWrapper(value, valueType, key2)
        return (self.node)

    def unity(self,data, option, FEntityName='', Ftype='entryList'):
        '''
        unity used for head or entry body with option as input.
        :param data:
        :param option:
        :param FEntityName:
        :param Ftype:
        :return:
        '''
        ncount = len(data)
        node = {}
        if ncount > 0:
            for i in data:
                node = model_Item(node, i)
            # 是否为表头
            if Ftype == 'head':
                option["Model"] = node
            else:
                option["Model"][FEntityName] = node
        return (option)
    def unityNode(self,data, FEntityName='', Ftype='entryList'):
        '''
        unitNode used for entryList without option as input parameters.s
        :param data:
        :param FEntityName:
        :param Ftype:
        :return:
        '''
        ncount = len(data)
        node = {}
        if ncount > 0:
            for i in data:
                node = model_Item(node, i)
        return (node)

    def tailUnity(self,Ftype='entryList', FEntityName='FEntityAuxPty', FListCount=1):
        '''
        tail Unity means one row the property setting without option
        :param Ftype:
        :param FEntityName:
        :param FListCount:
        :return:
        '''
        self.Ftype =Ftype
        self.FEntityName =FEntityName
        self.FListCount =FListCount
        data = self.queryData(Ftype=self.Ftype,FEntityName=self.FEntityName, FListCount=self.FListCount)
        res = self.unityNode(data=data, FEntityName=self.FEntityName, Ftype=self.Ftype)
        return (res)

    def tail(self,option,  Ftype='entryList',FEntityName='FEntityAuxPty'):
        '''
        tail mean model tail part represent as a list object.
        :param option:
        :param Ftype:
        :param FEntityName:
        :return:
        '''
        self.option = option
        self.Ftype = Ftype
        self.FEntityName =FEntityName
        data = self.tailCount(Ftype=self.Ftype, FEntityName=self.FEntityName)
        ncount = len(data)
        if ncount > 0:
            res = []
            for i in data:
                item = self.tailUnity(Ftype=self.Ftype, FEntityName=self.FEntityName,
                                       FListCount=i['FListCount'])
                res.append(item)
            self.option['Model'][self.FEntityName] = res
        return (self.option)

    def head(self):
        data = self.queryData(Ftype='head', FEntityName='', FListCount=0)
        option = {}
        option = self.unity(data=data, option=option, FEntityName='', Ftype='head')
        return (option)

    def body(self,option,FEntityName='FSubHeadEntity'):
        self.option = option
        self.FEntityName =FEntityName
        data = self.queryData(Ftype='entry', FEntityName=self.FEntityName, FListCount=0)
        ncount = len(data)
        self.option = self.unity(data=data, option=self.option, FEntityName=self.FEntityName, Ftype='entry')
        return (self.option)

    def bodySet(self,option):
        self.option =option
        dataSheet = self.bodySheet(Ftype='entry')
        for sheet in dataSheet:
            self.option = self.body(option=self.option,FEntityName=sheet['FEntityName'])
        return (self.option)

    def tailSet(self,option):
        self.option = option
        tailSheet = self.bodySheet(Ftype='entryList')
        for i in tailSheet:
            self.option = self.tail(option=self.option, Ftype='entryList',
                                FEntityName=i['FEntityName'])
            #print('bug2')
            #print(i)
            #print(self.option)
        return (self.option)

    def dataGen(self):
        # bill head
        option = self.head()
        # bill body
        option = self.bodySet(option=option)
        # tailList
        option = self.tailSet(option=option)
        return (option)
if __name__ =='__main__':
    pass















