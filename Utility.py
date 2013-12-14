import json

__name__ = "Utility"

class MyFile():
    def __init__(self, fileLocation):
        self.loc = fileLocation

    def Open(self):
        file = open(self.loc, 'r') 
        toParse = file.read()
        file.close()
        self.data = json.loads(toParse)

    def HasAttr(self, key):
        return key in self.data
        
    def Save(self):
        toSave = json.dumps(self.data, indent=2, separators=(',', ": "))
        file = open(self.loc, 'w')
        file.write(toSave)
        file.flush()
        file.close()

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