import urllib
import urllib2
import json
import re
from nerdnu.compile import write_json, write_raw

wiki_endpoint = "http://redditpublic.com/api.php?"

pp_ei = 50
pp_page = 50

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)


def query(**kwargs):
    args = {'format': 'json', 'action': 'query'}
    args.update(kwargs)
    q = urllib.urlencode(args)
    return json.load(urllib2.urlopen(wiki_endpoint + q))

def parse_template(name, data):
    data = data.split('\n')
    i = 0
    while i < len(data):
        if data[i] == '{{%s' % name:
            i += 1
            out = {}
            while i < len(data):
                m = re.match('^\|\s*(.+?)\s*=\s*(.*?)\s*$', data[i])
                if m:
                    k = m.group(1).strip().replace(' ', '_')
                    d = m.group(2).strip()
                    if not d in ('', '?'):
                        out[k] = d
                elif data[i].strip().startswith('}}'):
                    yield out
                    break
                
                i+=1
        i+=1

def get_template_usages(template_name):
    pageids = []
    
    print "... getting Template:%s usages" % template_name
    result = query(list='embeddedin', einamespace=0, eititle='Template:%s' % template_name, eilimit=pp_ei)
    while 'query-continue' in result:
        pageids += [c['pageid'] for c in result['query']['embeddedin']]
        result = query(list='embeddedin', einamespace=0, eititle='Template:Creation', eilimit=pp_ei, eicontinue=result['query-continue']['embeddedin']['eicontinue'])
    pageids += [c['pageid'] for c in result['query']['embeddedin']]
    
    data = []
    
    args = {
        'prop': 'revisions', 
        'rvprop': 'content'
    }
    
    while len(pageids) > 0:
        args['pageids'], pageids = '|'.join(str(p) for p in pageids[:pp_page]), pageids[pp_page:]
        
        print "... grabbing some pages"
        result = query(**args)
        
        for pid, v in result['query']['pages'].iteritems():
            d = v['revisions'][0]['*']
            for c in parse_template(template_name, d):
                c['page_title'] = v['title']
                data.append(c)
    
    print "Got %d usages of Template:%s" % (len(data), template_name)
    return data
    

def get_creations():
    usages = get_template_usages('Creation')
    for c in usages:
    
        #1. title
        if c.get('title', '').lower() in ('', '{{pagename}}'):
            c['title'] = c['page_title']
        
        #2. coords
        coords = c.get('coordinates', '')
        
        m = re.match('^{{Carto[^\|]*\|(.*?)}}$', coords)
        if m:
            props = dict([i.split('=') for i in m.group(1).split('|')])
            c['coordinates_normal'] = (int(props['x']), int(props['z']))
            if 'r' in props:
                c['map_revision'] = int(props['r'])
        else:
            m = re.findall('([\-\+]?[0-9]+)', coords)
            if len(m) in (2,3):
                c['coordinates_normal'] = (int(m[0]), int(m[-1]))
            else:
                #print "warning: couldn't normalise coords on %s" % c['page_title']
                pass
        
        #3. map revision
        
        if 'map_revision' in c:
            try:
                c['map_revision'] = int(c['map_revision'])
            except:
                print "skipping %s: unable to normalise map revision: %s" % (c['page_title'], c['map_revision'])
                continue
        else:
            print "skipping %s: no map revision defined" % c['page_title']
            continue

        #4. server
        for n in ("creative", "survival", "pve"):
            if n in c.get('server', '').lower():
                c['server'] = n
                break
        
        if not 'server' in c:
            print "skipping %s: no server listed" % c['page_title']
            continue

        """#5. image
        image = c.get('image', '')
        m = re.match('^\[\[Image:([^\|]*)\|?.*\]\]$', image.replace('File:', 'Image:'))
        if m:
            img = removeNonAscii(m.group(1))
            print "Getting %s" % img
            result2 = query(prop='imageinfo', titles='Image:%s' % img, rvprop='content', iiprop='url')
            
            tmp = result2['query']['pages'].values()[0]
            if 'imageinfo' in tmp:
                new['image'] = tmp['imageinfo'][0]['url']
            else:
                print "... doesn't exist!"""

        yield c


def get_grouped_creations():
    new = {}
    for c in get_creations():
        k = (c['server'], c['map_revision'])
        if k in new:
            new[k].append(c)
        else:
            new[k] = [c,]
    return new

def compile():
    #1. creations
    print "... fetching creations"
    creations = get_grouped_creations()
    current = {}
    
    for s in ('Creative', 'Survival', 'PvE'):
        print "... fetching %s map rev" % s
        result = query(titles="Template:Current %s map revision" % s, prop="revisions", rvprop="content")
        current[s.lower()] = int(result['query']['pages'].values()[0]['revisions'][0]['*'])
        
        print "... writing %s creations" % s
        for i in range(1, current[s.lower()]+1):
            k = (s.lower(), i)
            out = creations.get(k, [])
            out = sorted(out, key = lambda a: a['title'])
            write_json('creations/%s_%s.json' % k, out)
    
    #2. map rev
    print "... writing current revisions"
    write_json('current_rev.json', current)
    
    
    #3. rules
    print "... fetching rules"
    result = query(action='parse', page='Rules', prop='text')
    html = result['parse']['text']['*']
    html = re.sub('<span class="editsection">.*?</span>', '', html) #remove edit links
    html = re.sub('<a href="/wiki/', '<a href="http://redditpublic.com/wiki/', html) #fix internal links
    header_changes = {1:3, 3:4, 4:5}
    html = re.sub('\<(\/?)h([0-9]{1})\>', lambda m: '<%sh%d>' % (m.group(1), header_changes.get(int(m.group(2)), int(m.group(2)))), html) #Fix headers...
    #html = re.sub('<a href.*?>(.*?)</a>', '\\1', html) #remove internal links
    html = "".join(i for i in html if ord(i)<128)

    
    print "... writing rules"
    write_raw('rules.html', html.encode('utf-8'))
    
    print "... done"

#print json.dumps(get_grouped_creations(), )
#regenerate_json()
