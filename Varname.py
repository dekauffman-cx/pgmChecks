class Varname:
    """ Holds the variables and methods for passing the argument into the various 
        functions. this made argument passing much more flexible"""
    varDict = {}
    varList = []
    fileDict = {}
    noDefList = []
    def __init___(self):
        self.varDict = {}
        self.varList = []
        self.fileDict = {}
        self.noDefList = [] 

    def setVarList(self, strVar):
        self.varList.append(strVar)

    def setVarDict(self, strVar):
        if self.varDict.has_key(strVar):
            self.varDict[strVar] += 1
        else:
            self.varDict[strVar] = 0

    def setFileDict(self, dir, dict):
        self.fileDict[dir] = dict

    def getVarlist(self):
        return self.varList

    def getVarDict(self):
        return self.varDict

    def getFileDict(self):
        return self.fileDict
        
    def varInVarList(self, strVar):
        return strVar in self.varList
    
    def varInVarDict(self, strVar):
        return self.varDict.has_key(strVar)
    
    def varNotDefined(self, strVar):
        self.noDefList.append(strVar)

    def getNoDefList(self):
        return self.noDefList
