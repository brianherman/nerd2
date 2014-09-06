from nerdnu import app
from nerdnu.compile import write_json
import re, datetime, operator, gzip, sys, os
import glob
import json
import os

actions = {
        'login': re.compile('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) \[INFO\] ([\xa7A-z0-9]*) \[/[0-9.]{4,15}:\d*\]'),
        'logout': re.compile('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) \[INFO\] ([\xa7A-z0-9]*) lost connection')
}

class Player:
    name = ''
    total = 0
    days = 0

def parse_file(handle, online):
    totals = {}
    for line in handle.readlines():
        regex = None
        action = None
        player = None
        time = None
        for action in actions:
            if actions[action].match(line):
                regex = actions[action]
                break

        if regex is not None:
            # Get the user's name and parse the datetime
            data = regex.split(line)
            player = unicode(data[7], 'utf-8')
            if player.startswith(u'\xa7'):
                player = player[2:]
                if player[-2] == u'\xa7':
                    player = player[:-2]
                if player[-1] == u'\xa7':
                    player = player[:-1]

            time = datetime.datetime(int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]))

            # Now do things!
            if action is 'login':
                online[player] = time
            elif action is 'logout':
                if player not in totals:
                    totals[player] = 0
                if player in online:
                    delta = time - online[player]
                    totals[player] += delta.seconds
    
    return totals

def merge_totals(a, b):
    for k, v in b.iteritems():
        a[k] = a.get(k, 0) + v
    return a

def compile():
    days = 7
    show = 100
    
    out = {}
    cutoff = datetime.datetime.today() - datetime.timedelta(days)
    
    #'creative', 'survival', 
    for n in ('creative', 'survival', 'pve'):
        print "... reading %s logs" % n
        totals = {}
        online = {}
        relevant_files = []
        
        for fname in sorted(glob.glob(os.path.join(app.config['HOME_DIR'], 'logs/%s/*' % n))):
            m = re.match('server-(\d{4})-(\d{2})-(\d{2})-(\d{2}):(\d{2}):(\d{2}).log.gz$', os.path.basename(fname))
            if m:
                d = datetime.datetime(*[int(i) for i in m.groups()])
                if d > cutoff:
                    with gzip.open(fname) as handle:
                        x = parse_file(handle, online)
                        totals = merge_totals(totals, x)
        
        sort = [{'name': i[0], 'hours':(i[1]/3600)} for i in sorted(totals.iteritems(), key=lambda p: p[1], reverse=True)]
        
        out[n] = sort[:show]
    
    write_json('top_players.json', out)
    
    print "... done"
