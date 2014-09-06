import socket
import struct
import json
import re
import os

from nerdnu import app
from nerdnu.compile import write_json

class MCQuery:
    id = 0
    retries = 0
    max_retries = 3
    timeout = 3
    
    def __init__(self, host, port, **kargs):
        self.addr = (host, port)
        if 'max_retries' in kargs:
            self.max_retries = kargs['max_retries']
        if 'timeout' in kargs:
            self.timeout = kargs['timeout']
       
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.timeout)
        self.handshake()
    
    def write_packet(self, type, payload):
        o = '\xFE\xFD' + struct.pack('>B', type) + struct.pack('>l', self.id) + payload
        self.socket.sendto(o, self.addr)
    
    def read_packet(self):
        buff = self.socket.recvfrom(2048)[0]
        type = struct.unpack('>B', buff[0])[0]
        id   = struct.unpack('>l', buff[1:5])[0]
        return type, id, buff[5:]
    
    def handshake(self):
        self.id += 1
        self.write_packet(9, '')
        try:
            type, id, buff = self.read_packet()
        except:
            self.retries += 1
            if self.retries == self.max_retries:
                raise Exception('Retry limit reached - server down?')
            return self.handshake()
        
        self.retries = 0
        self.challenge = struct.pack('>l', int(buff[:-1]))
    
    def basic_stat(self):
        self.write_packet(0, self.challenge)
        try:
            type, id, buff = self.read_packet()
        except:
            self.handshake()
            return self.basic_stat()
        
        data = {}
        
        #I don't seem to be receiving this field...
        #data['ip'] = socket.inet_ntoa(buff[:4])[0]
        #buff = buff[4:]
        
        #Grab the first 5 string fields
        data['motd'], data['gametype'], data['map'], data['numplayers'], data['maxplayers'], buff = buff.split('\x00', 5)
        
        #Unpack a big-endian short for the port
        data['hostport'] = struct.unpack('<h', buff[:2])[0]
        
        #Grab final string component: host name
        data['hostname'] = buff[2:-1]
        
        #Encode integer fields
        for k in ('numplayers', 'maxplayers'):
            data[k] = int(data[k])

        return data
    
    def full_stat(self):
        #Pad request to 8 bytes
        self.write_packet(0, self.challenge + '\x00\x00\x00\x00')
        try:
            type, id, buff = self.read_packet()
        except:
            self.handshake()
            return self.full_stat()    
        
        #Chop off useless stuff at beginning
        buff = buff[11:]
        
        #Split around notch's silly token
        items, players = buff.split('\x00\x00\x01player_\x00\x00')
        
        #Notch wrote "hostname" where he meant to write "motd"
        items = 'motd' + items[8:] 
        
        #Encode (k1, v1, k2, v2 ..) into a dict
        items = items.split('\x00')
        data = dict(zip(items[::2], items[1::2])) 

        #Remove final two null bytes
        players = players[:-2]
        
        #Split player list
        if players: data['players'] = sorted([re.sub('\xa7.{1}', '', p) for p in players.split('\x00')], key=str.lower)
        else:       data['players'] = []
        
        
        #Encode ints
        for k in ('numplayers', 'maxplayers', 'hostport'):
            data[k] = int(data[k])
        
        #Parse 'plugins'
        s = data['plugins']
        s = s.split(': ', 1)
        data['server_mod'] = s[0]
        if len(s) == 1:
            data['plugins'] = []
        elif len(s) == 2:
            data['plugins'] = s[1].split('; ')

        return data


def compile():
    out = {}
    for n in ('creative', 'survival', 'pve'):
        props = {
            'server-ip': '',
            'enable-query': 'false',
            'query.port': 25565}
        f = open(os.path.join(app.config['HOME_DIR'], n, 'server.properties'), 'r')
        for l in f:
            for p in props.keys():
                if l.startswith(p):
                    props[p] = l[len(p)+1:].strip()
        
        if props['enable-query'] == 'true':
            try:
                print "... querying %s" % n
                q = MCQuery(props['server-ip'], int(props['query.port']))
                d = q.full_stat()
                print "... success!"
                d = {
                    'up': True,
                    'numplayers': d['numplayers'],
                    'maxplayers': d['maxplayers'],
                    'players': d['players']
                }
            except:
                d = {'up': False}
                print "... failed"
                #raise
        else:
            d = {'up': False}
            print "... query not enabled for %s!" % n
        out[n] = d

    write_json('statuses.json', out)    
    
    print "... done"
