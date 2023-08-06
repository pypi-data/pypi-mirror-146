from ticsummary import databaseMYSQL, backWorking

from PyQt6.QtCore import QObject, pyqtSignal
import numpy as np


def loadDataById(id,sqlParameters,connector = None):
    if connector == None:
        connector = databaseMYSQL.openConnection(sqlParameters)
    dataB1 = databaseMYSQL.getRecordByIdFirstBank(sqlParameters.table, connector, id)
    dataB2 = databaseMYSQL.getRecordByIdSecondBank(sqlParameters.table, connector, id)
    return (dataB1.matrix,dataB1.timeslice,dataB2.matrix,dataB2.timeslice,dataB1,dataB2)
        
def loadDataByIdRange(id,count,sqlParameters,connector = None):
    if connector == None:
        connector = databaseMYSQL.openConnection(sqlParameters)
    idList = range(id,id+count)
    dataB1List = databaseMYSQL.getRecordByIdListFirstBank(sqlParameters.table, connector, idList)
    dataB2List = databaseMYSQL.getRecordByIdListSecondBank(sqlParameters.table, connector, idList)
    result = list()
    for i in range(0,np.size(dataB1List)):  #(dataB1.matrix,dataB1.timeslice,dataB2.matrix,dataB2.timeslice,dataB1,dataB2)
        result.append((dataB1List[i].matrix,dataB1List[i].timeslice,dataB2List[i].matrix,dataB2List[i].timeslice))
    return result
    

'''def sumData(dataB1List,dataB2List):
    sumDataB1 = np.zeros(shape=(np.size(dataB1List[0].matrix,0),np.size(dataB1List[0].matrix,1)))
    sumDataB2 = np.zeros(shape=(np.size(dataB2List[0].matrix,0),np.size(dataB2List[0].matrix,1)))
    for i in range(count):
        sumDataB1 += dataB1List[i].matrix
        sumDataB2 += dataB2List[i].matrix
    return (sumDataB1,dataB1List[0].timeslice,sumDataB2,dataB2List[0].timeslice)'''