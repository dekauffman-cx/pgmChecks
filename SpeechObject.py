class SpeechObject:
    """ voiceList: organizes by directory name """
    voiceDict = {}
    problemList = []
    def __init__(self):
        self.problemList = []
        self.voiceDict = {}
         
    def exists(self, p):
        if  p in self.voiceDict:
            return True
        else:
            return False
    
    def insert(self, d):
        self.voiceDict = d
        print(self.voiceDict) # temporarily adding to ensure what we're doing is right

    def voiceIssues(self, wav):
        self.problemList.append(wav)
        
    def retrieve(self): 
        return self.voiceDict
    
    