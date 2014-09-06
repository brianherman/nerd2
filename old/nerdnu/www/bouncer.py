import urllib
import json

API_ADDRESS = 'http://mcbouncer.com/api'

class MCBouncer():
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
    
    #__getattr__ = lambda self, method: lambda *args: json.load(urllib.urlopen('/'.join([API_ADDRESS, method, self.API_KEY] + [urllib.quote(a, "") for a in args])))
    
    def __getattr__(self, method):
        def inner(*args):
            args = [urllib.quote(a, "") for a in args]
            addr = '/'.join([API_ADDRESS, method, self.API_KEY] + args)
            reply = urllib.urlopen(addr)
            return json.load(reply)
        return inner
