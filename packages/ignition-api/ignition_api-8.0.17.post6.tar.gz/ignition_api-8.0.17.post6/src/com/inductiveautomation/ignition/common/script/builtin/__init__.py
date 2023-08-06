__all__ = ["AbstractOPCUtilities", "DatasetUtilities", "SProcCall", "SystemUtilities"]

from com.inductiveautomation.ignition.common import BasicDataset, Dataset
from com.inductiveautomation.ignition.common.script.message import Request
from java.lang import Object
from java.util import Locale
from org.python.core import PyObject


class AbstractOPCUtilities(Object):
    def browseServer(self, opcServer, nodeId):
        return [AbstractOPCUtilities.PyOPCTag(opcServer, nodeId, None, self.__class__)]

    def getServers(self):
        pass

    def getServerState(self, opcServer):
        pass

    def isServerEnabled(self, serverName):
        pass

    def readValue(self, opcServer, itemPath):
        pass

    def readValues(self, opcServer, itemPaths):
        pass

    def setServerEnabled(self, serverName, enabled):
        pass

    def writeValue(self, *args, **kwargs):
        pass

    def writeValues(self, *args, **kwargs):
        pass

    class PyOPCTag(PyObject):
        _displayName = None
        _elementType = None
        _nodeId = None
        _serverName = None

        def __init__(self, serverName, nodeId, displayName, elementType):
            self._serverName = serverName
            self._nodeId = nodeId
            self._displayName = displayName
            self._elementType = elementType
            super(AbstractOPCUtilities.PyOPCTag, self).__init__()

        def __findattr_ex__(self, name):
            pass

        def getDisplayName(self):
            return self._displayName

        def getElementType(self):
            return self._elementType

        def getNodeId(self):
            return self._nodeId

        def getServerName(self):
            return self._serverName


class DatasetUtilities(Object):
    @staticmethod
    def addColumn(*args):
        pass

    @staticmethod
    def addRow(*args):
        pass

    @staticmethod
    def addRows(*args):
        pass

    @staticmethod
    def appendDataset(ds1, ds2):
        pass

    @staticmethod
    def clearDataset(ds):
        pass

    @staticmethod
    def dataSetToExcel(headerRow, datasets):
        pass

    @staticmethod
    def dataSetToExcelBytes(headerRow, objects, nullsEmpty, sheetNames):
        pass

    @staticmethod
    def dataSetToExcelStreaming(headerRow, objects, out, nullsEmpty):
        pass

    @staticmethod
    def dataSetToHTML(headerRow, ds, title):
        pass

    @staticmethod
    def dataSetToHTMLStreaming(headerRow, ds, title, fw):
        pass

    @staticmethod
    def deleteRow(ds, row):
        pass

    @staticmethod
    def deleteRows(ds, rows):
        pass

    @staticmethod
    def filterColumns(dataset, columns):
        pass

    @staticmethod
    def formatDates(dataset, format, locale=Locale.US):
        pass

    @staticmethod
    def fromCSV(csv):
        pass

    @staticmethod
    def fromCSVJava(csv):
        pass

    @staticmethod
    def getColumnHeaders(ds):
        pass

    @staticmethod
    def insertColumn(*args):
        pass

    @staticmethod
    def insertRow(*args):
        pass

    @staticmethod
    def setValue(*args):
        pass

    @staticmethod
    def sort(ds, keyColumn, ascending=None, naturalOrdering=None):
        pass

    @staticmethod
    def toCSV(*args, **kwargs):
        pass

    @staticmethod
    def toCSVJava(ds, showHeaders, forExport, localized=False):
        pass

    @staticmethod
    def toCSVJavaStreaming(ds, showHeaders, forExport, sw, localized):
        pass

    @staticmethod
    def toDataSet(*args):
        pass

    @staticmethod
    def toExcel(*args, **kwargs):
        pass

    @staticmethod
    def toJSONObject(data):
        pass

    @staticmethod
    def toPyDataSet(dataset):
        pass

    @staticmethod
    def updateRow(ds, row, changes):
        pass

    class PyDataSet(Dataset):
        _ds = None

        def __init__(self, ds=None):
            self._ds = ds

        def __getitem__(self, item):
            pass

        def __iter__(self):
            pass

        def __len__(self):
            pass

        def getColumnCount(self):
            pass

        def getColumnIndex(self, name):
            pass

        def getColumnName(self, col):
            pass

        def getColumnNames(self):
            pass

        def getColumnType(self, col):
            pass

        def getColumnTypes(self):
            pass

        def getPrimitiveValueAt(self, row, col):
            pass

        def getQualityAt(self, row, col):
            pass

        def getRowCount(self):
            pass

        def getValueAt(self, *args):
            pass


class SProcCall(Object):
    def _getParams(self):
        pass

    def _getReturnParam(self):
        pass

    def getDatasource(self):
        pass

    def getOutParamValue(self, param):
        """Returns the value of the previously registered out-parameter.

        Args:
            param (object): Index (int) or name (str) of the previously
                registered out-parameter.

        Returns:
            object: The value of the previously registered
                out-parameter.
        """
        print(self, param)
        return 0

    def getProcedureName(self):
        pass

    def getResultSet(self):
        """Returns a dataset that is the resulting data of the stored
        procedure, if any.

        Returns:
            Dataset: The dataset that is the resulting data of the
                stored procedure, if any.
        """
        print(self)
        return BasicDataset()

    def getReturnValue(self):
        """Returns the return value, if registerReturnParam had been
        called.

        Returns:
             int: The return value, if registerReturnParam had been
                called.
        """
        print(self)
        return 0

    def getTxId(self):
        pass

    def getUpdateCount(self):
        """Returns the number of rows modified by the stored procedure,
        or -1 if not applicable.

        Returns:
             int: The number of rows modified by the stored procedure,
                or -1 if not applicable.
        """
        print(self)
        return 1

    def isSkipAudit(self):
        pass

    def registerInParam(self, param, typeCode, value):
        """Registers an in parameter for the stored procedure.

        Args:
            param (object): Index (int starting at 1, not 0), or name
                (str).
            typeCode (int): Type code constant.
            value (object): Value of type typeCode.
        """
        print(self, param, typeCode, value)

    def registerOutParam(self, param, typeCode):
        """Registers an out parameter for the stored procedure.

        Args:
            param (object): Index (int starting at 1, not 0), or name
                (str).
            typeCode (int): Type code constant.
        """
        print(self, param, typeCode)

    def registerReturnParam(self, typeCode):
        """Use this function to specify the datatype of the returned
        value.

        Args:
            typeCode (int): Type code constant.
        """
        print(self, typeCode)

    def setDatasource(self, datasource):
        pass

    def setProcedureName(self, procedureName):
        pass

    def setSkipAudit(self, skipAudit):
        pass

    def setTxId(self, txId):
        pass

    class SProcArg(Object):
        def getParamType(self):
            pass

        def getValue(self):
            pass

        def isInParam(self):
            pass

        def isOutParam(self):
            pass

        def setParamType(self, paramType):
            pass

        def setValue(self, value):
            pass

        def toString(self):
            pass

    class SProcArgKey(Object):
        def getParamIndex(self):
            pass

        def getParamName(self):
            pass

        def hashCode(self):
            pass

        def isNamedParam(self):
            pass

        def toString(self):
            pass


class SystemUtilities(Object):
    def __init__(self, timeout):
        self.timeout = timeout

    @staticmethod
    def logger(loggerName):
        pass

    @staticmethod
    def parseTranslateArguments(*args, **kwargs):
        pass

    class RequestImpl(Object, Request):
        def __init__(self, timeout):
            self.timeout = timeout

        def block(self):
            pass

        def cancel(self):
            pass

        def checkTimeout(self):
            pass

        def compose(self, requestWatchers):
            pass

        def dispatchFunc(self):
            pass

        def finishExceptionally(self, e):
            pass

        def finishSuccessfully(self, value):
            pass

        def get(self):
            pass

        def getError(self):
            pass

        def onError(self, func):
            pass

        def onSuccess(self, func):
            pass
