import configparser

class config(object):
    def __init__(self, ConfigName):
        self.config = configparser.ConfigParser()
        self.config.read(ConfigName)
        
    def getFindMatchesUrl(self):
        return self.config['api']['findMatches']
    
    def getMatchesUrl(self):
        return self.config['api']['matches']
    
    def getParsedMatchesUrl(self):
        return self.config['api']['parsedMatches']
        
if __name__ == '__main__':
    c = config('conf\\config.ini')
    u = c.getMatchesUrl()
    
    print(u)
    print(u.replace("{match_id}", '12345'))
    print(u)
    