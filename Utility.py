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
        data = json.dumps(self.data, indent=2, separators=(',', ": "))
        print data