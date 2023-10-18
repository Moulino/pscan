import json

PORT_FILE = 'ports.json'

class InfoPorts:
    """ Classe permettant de récupérer la description d'un port """
    
    def __init__(self):
        self._ports = {}
        self.load()
        
        
    def load(self):
        with open(PORT_FILE, 'r') as f:
            self._ports = json.load(f)
            
            
    def description_for(self, port: int):
        
        if str(port) in self._ports:
            _p = self._ports[str(port)]
            
            if type(_p) == list:
                return _p[0]['description']
            elif type(_p) == dict:
                return _p['description']
            
        return 'Unknown'