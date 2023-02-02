from collections import defaultdict

class SpeechObject:
    """ voiceDict: organizes by directory name """
    voiceDict = {} 
    def __init__(self):
        self.voiceDict = {}
          
    def exists(self, p):
        if self.voiceDict.has_key(self, p):
            return True
        else:
            return False
    def insertOuter(self, d):
        self.voiceDict.update(d)
        
    def innerDict(self, p, inner):
        self.voiceDict[p] = inner
        print("obj: " + self.voiceDict) # temporarily adding to ensure what we're doing is right

    def retrieve(self): 
        return self.voiceDict