import json
import string
import copy
__name__ = "Utility"

class MyFile():
    def __init__(self, fileLocation):
        self.loc = fileLocation

    def Open(self, perLoc):
        self.mod  = False
        self.perLoc = perLoc
        self.tempLoc = None
        file = open(self.loc, 'r') 
        toParse = file.read()
        file.close()
        jsonSafe = ""
        for line in toParse.splitlines(True):
            if '//' not in line:
                jsonSafe += line
        self.data = json.loads(jsonSafe)
        self.origData = copy.deepcopy(self.data)
    
    def Tuple(self):
        SingleToTuple(self.data)
        self.data = (self.data,False,False)
    
    def HasAttr(self, key):
        return key in self.data
        
    def Save(self):
        toSave = json.dumps(self.data, indent=2, separators=(',', ": "))
        file = open(self.loc, 'w')
        file.write(toSave)
        file.flush()
        file.close()
        
    def Modified(self):
        pass

        
def TryToParse(string):
    try:
        if float(string) == int(string):
            return int(string)
        else:
            return float(string)
    except:
        if string == "false" or "False":
            return False
        elif string == "true" or "True":
            return True
        else:
            return string
            
def SingleToTuple(data):
    if type(data) is dict:
        for key, val in  data.iteritems():
            if type(val) is dict or type(val) is list:
                SingleToTuple(val)
            data[key] = (val,False,False)
    elif type(data) is list:
        for i in range(len(data)):
            if type(data[i]) is dict or type(data[i]) is list:
                    SingleToTuple(data[i])
            data[i] = (data[i],False,False)
    else:
        raise Error
        
def COUT(obj):
    print str(type(obj))+" "+str(obj)