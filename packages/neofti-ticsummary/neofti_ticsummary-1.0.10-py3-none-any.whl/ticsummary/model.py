from tracemalloc import start
from ticsummary import dataTIC, databaseMYSQL, inputDataHandler
from ticsummary.ui.MainWindow import MainWindow, ModeInterface as MWModeInterface
from ticsummary.ui.ConnectionConfigurationDialog import ConnectionConfiguration
from ticsummary.ui.OpenSqlDataDialog import OpenSQLData
from ticsummary import databaseMYSQL
from ticsummary.backWorking import factoryThreadByTask
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox

class Model(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.__initView__()
        self.__initSignal__()
        self.sqlParameters = None
        self.mainWindow.show()
        
        self.profileXDescriptionDevice = dataTIC.DescriptionDevice("profileX",0,31)
        self.profileYDescriptionDevice = dataTIC.DescriptionDevice("profileY",32,63)
    def __initView__(self):
        self.mainWindow = MainWindow()
        
    def __initSignal__(self):
        self.mainWindow.ui.comboBoxType.currentIndexChanged.connect(self.__typeChanged)
        self.mainWindow.ui.actionConnectionSqlDatabase.triggered.connect(self.openConnectionConfiguration)
        self.mainWindow.ui.actionFrom_sql_database.triggered.connect(self.startOpenSQLData)
        self.mainWindow.sigIterationValueId.connect(self.iterationData)
        self.mainWindow.sigSetNewId.connect(self.setIdData)
        #self.mainWindow.connectSignalIterationValueId(self.iterationData)
        #self.mainWindow.ui.comboBoxListData.currentTextChanged.connect(self.loadDataByIdAndPlot)
    
    def __del__(self):
        self.connector.close()
    
    def openConnectionConfiguration(self):
        connectionConfigurationDialog = ConnectionConfiguration(self.sqlParameters)
        connectionConfigurationDialog.setModal(True)
        connectionConfigurationDialog.exec()
        if connectionConfigurationDialog.result() == QtWidgets.QDialog.DialogCode.Accepted:
            self.mainWindow.setInfinityProgress(True)
            self.sqlParameters = connectionConfigurationDialog.getNewParameters()
            self.mainWindow.setMode(MWModeInterface.MANUAL)
            self.connector = databaseMYSQL.openConnection(self.sqlParameters)
            self.countRecordsInDB = databaseMYSQL.getCountRecords(self.sqlParameters.table, self.connector)
            self.__setValueCurrentId(1)
            self.__backThreadLoadData__(self.currentIdData,self.connector)
            self.__plotData__()
            #self.controllerBWTask = factoryThreadByTask(self.__loadNewConnection__,self.__setNewConnection__,sqlParameters=self.sqlParameters)
            #self.controllerBWTask.start()

    def __loadNewConnection__(self,sqlParameters):
        self.listData = databaseMYSQL.getListId(self.sqlParameters)

    def __setNewConnection__(self):
        self.mainWindow.setMode(MWModeInterface.MANUAL)
        self.connector = databaseMYSQL.openConnection(self.sqlParameters)
        self.mainWindow.setIndexListData(map(str,self.listData['id_RUN']))
        self.__setValueCurrentId(0)

    def loadDataByIdAndPlot(self,id:str, connector=None):
        i = 0
        if connector == None:
            self.controllerBWTask = factoryThreadByTask(self.__backThreadLoadData__,self.__plotData__,id=int(id),connector=self.connector)
        else:
            self.controllerBWTask = factoryThreadByTask(self.__backThreadLoadData__,self.__plotData__,id=int(id),connector=connector)
        self.controllerBWTask.start()

    def __backThreadLoadData__(self,id,connector):
        self.dataB1 = databaseMYSQL.getRecordByIdFirstbank(self.sqlParameters.table, self.connector, id)
        self.dataB2 = databaseMYSQL.getRecordByIdSecondBank(self.sqlParameters.table, self.connector, id)
        
    def __plotData__(self):
        profileX1Data = inputDataHandler.getMatrixByFromToFilter(self.dataB1.matrix, self.profileXDescriptionDevice.channelFrom, self.profileXDescriptionDevice.channelTo)
        profileY1Data = inputDataHandler.getMatrixByFromToFilter(self.dataB1.matrix, self.profileYDescriptionDevice.channelFrom, self.profileYDescriptionDevice.channelTo)
        profileX2Data = inputDataHandler.getMatrixByFromToFilter(self.dataB2.matrix, self.profileXDescriptionDevice.channelFrom, self.profileXDescriptionDevice.channelTo)
        profileY2Data = inputDataHandler.getMatrixByFromToFilter(self.dataB2.matrix, self.profileYDescriptionDevice.channelFrom, self.profileYDescriptionDevice.channelTo)
        self.mainWindow.setData(profileX1Data,
            float(self.dataB1.timeslice/(10**6)),
            profileY1Data,
            float(self.dataB1.timeslice/(10**6)),
            profileX2Data,
            float(self.dataB2.timeslice/(10**6)),
            profileY2Data,
            float(self.dataB2.timeslice/(10**6)))
        self.mainWindow.flagControlKeysOff = False

    def iterationData(self,it):
        self.mainWindow.flagControlKeysOff = True
        if (self.currentIdData + it > -1 or self.currentIdData + it < self.countRecordsInDB):
            self.__setValueCurrentId(self.currentIdData + it)
            self.controlerBWTask = factoryThreadByTask(self.__backThreadLoadData__, self.__plotData__,id=self.currentIdData,connector=self.connector)
            self.controlerBWTask.start()
            #self.__backThreadLoadData__(self.currentIdData,self.connector)
            #self.__plotData__()
        #self.mainWindow.flagControlKeysOff = False

    def setIdData(self,value):
        self.mainWindow.flagControlKeysOff = True
        #if value <= -1:

        #if value >= self.countRecordsInDB:

        if (value > -1 or value < self.countRecordsInDB):
            self.__setValueCurrentId(value)
            self.__backThreadLoadData__(self.currentIdData,self.connector)
            self.__plotData__()
        self.mainWindow.flagControlKeysOff = False
            

    def __setValueCurrentId(self,value):
        self.currentIdData = value
        self.mainWindow.ui.lineEditId.setText(str(value))

    def updateSizeDB(self):
        self.countRecordsInDB = databaseMYSQL.getCountRecordsByParameters(self.sqlParameters)

    def __typeChanged(self,id):
        if id == 0:
            if self.realTimeModeOn :
                self.realTimeModeOn = False
                self.mainWindow.setMode(MWModeInterface.MANUAL)
                self.offRealTimeMode()    
        if id == 1:
            self.mainWindow.setMode(MWModeInterface.ONLINE)
            self.realTimeModeOn = True
            self.setRealTimeMode() 
    
    def setRealTimeMode(self):
        self.realTimeModeTimer = QtCore.QTimer()
        self.realTimeModeTimer.timeout.connect(self.__doTimerRealTimeMode__)
        self.realTimeModeTimer.start(1000)
        self.lastCount = 0

    def offRealTimeMode(self):
        self.realTimeModeTimer.stop()

    def __doTimerRealTimeMode__(self):
        #tempconnector = databaseMYSQL.openConnection(self.sqlParameters)
        count = databaseMYSQL.getCountRecords(self.sqlParameters.table,self.connector)
        if count > self.lastCount:
            self.lastCount = count
            self.loadDataByIdAndPlot(count-1)
    
    def startOpenSQLData(self):
        self.mainWindow.setInfinityProgress()
        self.handlerTaskOpenData = runTask(self.taskOpenData,self.endOpenSqlData)
        
    def taskOpenData(self):
        self.openSQLData = OpenSQLData(self.sqlParameters, lambda result: self.setNewListData(result))
        
    def endOpenSqlData(self):
        self.mainWindow.unsetInfinityProgress()
        self.openSQLData.show()

    def setNewConnectionParameters(self, parameters):
        self.sqlParameters = parameters
        
    def setNewListData(self, list):
        self.listData = list