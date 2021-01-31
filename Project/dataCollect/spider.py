import requests
import json

class spider(object):
    def __init__(self):
        pass
    
    @classmethod
    def GET(self, url, params=None, timeout=10):
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code != 200:
            raise Exception('status error')
        else:
            return json.loads(response.text)
        
        
if __name__ == '__main__':
    pass
