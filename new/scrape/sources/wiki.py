import re
import json
import urllib

from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from scrape.sources import Source




class WikiSource(Source):
    def _update_creation(self, name, server, revision, x, z):
        self.api_call("update_creation",
            name=name,
            server=server,
            revision=revision,
            x=x,
            z=z
        )

    def _query(self, **request_data):
        d0 = defer.Deferred()

        def _callback(d):
            d0.callback(json.loads(d.decode('utf8')))

        def _errback(e):
            d0.errback(e)

        args = {'format': 'json'}
        args.update(request_data)
        url = 'http://redditpublic.com/api.php?' + urllib.urlencode(args)
        #print url

        d1 = client.getPage(url)
        d1.addCallbacks(_callback, _errback)

        return d0

    def _get_html(self, page_name):
        return self._query(
            action='parse',
            page=page_name,
            prop='text')

    def _get_text(self, section=None, *page_names):
        d0 = defer.Deferred()

        def _callback(response_data_old):
            response_data = response_data_old['query']['pages'].values()
            #print response_data
            for p in response_data:
                try:
                    p['text'] = p['revisions'][0]['*']
                except exception.KeyError:
                    print "Page "+p['title']+" does not exist."
            d0.callback(response_data)

        def _errback(e):
            d0.errback(e)

        if section:
            d1 = self._query(
                action='query',
                titles='|'.join(page_names),
                prop='revisions',
                rvprop='content',
                rvsection=section)
        else:
            d1 = self._query(
                action='query',
                titles='|'.join(page_names),
                prop='revisions',
                rvprop='content')
        d1.addCallbacks(_callback, _errback)

        return d0

    def _get_usages(self, template_name, token=None):
        #print token
        pp_ei = 50

        d0 = defer.Deferred()

        def _callback(response_data):
            pages = []
            for p in response_data['query']['embeddedin']:
                pages.append(p['title'].encode('utf8'))

            if 'query-continue' in response_data:
                #print "looping"
                def _callback_accumulate(more_pages):
                    d0.callback(pages + more_pages)

                token = response_data['query-continue']['embeddedin']['eicontinue']
                d1 = self._get_usages(template_name, token)
                d1.addCallback(_callback_accumulate)
            else:
                #print "firing"
                # Fire off the chain of deferreds
                d0.callback(pages)

        def _errback(e):
            print e

        args = dict(
            action='query',
            list='embeddedin',
            einamespace=0,
            eititle='Template:%s' % template_name,
            eilimit=pp_ei,
        )
        if token:
            args['eicontinue'] = token
        d2 = self._query(**args)
        d2.addCallbacks(_callback, _errback)

        return d0

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        ### Grab rules (used for static rule page)
        d = self._get_html('Rules')
        d.addCallback(self._handle_rules)

        ### Grab IRC (used for static IRC page)
        d = self._get_html('IRC')
        d.addCallback(self._handle_irc)

        ### Grab IRC Quotes (used for community page)
        d = self._get_text(8, 'Bestof')
        d.addCallback(self._handle_quotes)

        ### Grab creations from Creative page
        d = self._get_text(None, "Creative")
        d.addCallback(self._handle_creative_creations)

        ### Grab current revisions
        pages = []
        for server in ("Creative", "Survival", "PvE"):
            pages.append("Template:Current %s map revision" % server)
        d = self._get_text(None, *pages)
        d.addCallback(self._handle_current_revisions)

        ### Grab usages of Template:Creation
        d = self._get_usages('Creation')
        d.addCallback(self._handle_global_creations)


    def _handle_rules(self, response_data):
        html = response_data['parse']['text']['*']

        ### Remove edit links
        html = re.sub('<span class="editsection">.*?</span>', '', html)

        ### Fix internal links
        html = re.sub('<a href="/wiki/', '<a href="http://redditpublic.com/wiki/', html)

        ### Change headers
        def header_callback(match):
            g = match.groups()
            changes = {
                "1": "3",
                "3": "4",
                "4": "5"
            }
            return '<%sh%s>' % (g[0], changes.get(g[1], g[1]))

        html = re.sub('\<(\/?)h([0-9]{1})\>', header_callback, html)

        ### Convert to UTF8
        html = html.encode('utf8')

        ### Store in DB
        self.api_call("update_cache", key="HTML_RULES", value=html)

    def _handle_irc(self, response_data):
        html = response_data['parse']['text']['*']

        ### Remove edit links
        html = re.sub('<span class="editsection">.*?</span>', '', html)

        ### Fix internal links
        html = re.sub('<a href="/wiki/', '<a href="http://redditpublic.com/wiki/', html)

        ### Change headers
        def header_callback(match):
            g = match.groups()
            changes = {
                "1": "3",
                "3": "4",
                "4": "5"
            }
            return '<%sh%s>' % (g[0], changes.get(g[1], g[1]))

        html = re.sub('\<(\/?)h([0-9]{1})\>', header_callback, html)

        ### Convert to UTF8
        html = html.encode('utf8')

        ### Store in DB
        self.api_call("update_cache", key="HTML_IRC", value=html)

    def _handle_quotes(self, response_data):
        data = response_data[0]['text'].splitlines(True)

        quotes = []
        quote_text = ""
        for line in data:
            if line[0] == " ":
                quote_text += "%s\n" % line.strip()
            elif quote_text:
                quotes.append(quote_text)
                quote_text = ""

        quotes = json.dumps(quotes)

        self.api_call("update_cache", key="IRC_QUOTES", value=quotes)

    def _handle_current_revisions(self, response_data):
        current_revisions = {}

        ### Parse response
        for response in response_data:
            m = re.match("Template:Current (\w+) map revision", response['title'])
            current_revisions[m.group(1).upper()] = int(response['text'])

        ### Store in DB
        for server, revision in current_revisions.iteritems():
            self.api_call("update_cache",
                key="CURRENT_REVISION_%s" % server,
                value=revision)

        ### Parse PvE templates
        pages = []
        for r in range(7, current_revisions['PVE']+1):
            pages.append("Template:PvE r%d" % r)
        d = self._get_text(*pages)
        d.addCallback(self._handle_pve_creations)

    def _handle_creative_creations(self, response_data):
        text = response_data[0]['text']

        revision = 0
        for line in text.split("\n"):
            m = re.match('===Warps \(revision (\d+)\)===', line)
            if m:
                revision = int(m.group(1))

            m = re.match("\* '''([^']+)''' \(\+?([\-\d]+), \d+, \+?([\-\d]+)\)", line)
            if m:
                self._update_creation(
                    m.group(1),
                    'creative',
                    revision,
                    int(m.group(2)),
                    int(m.group(3))
                )

    def _handle_pve_creations(self, response_data):
        for response in response_data:
            for name, carto_data in re.findall("([^\|\[]+)\]\]\s\{\{CartoP\|?([^}]+)\}\}", response['text']):
                carto_data = dict((d.split('=') for d in carto_data.split("|")))
                if name not in ('CoolTown', 'ExampleVille'):
                    self._update_creation(
                        name,
                        'pve',
                        int(carto_data['r']),
                        int(carto_data['x']),
                        int(carto_data['z'])
                    )

    def _handle_global_creations(self, pages):
        def _callback(response_data):
            for response in response_data:
                for g0 in re.findall('\{\{Creation\s*\n(.+?)\n\s*\}\}', response['text'], flags=re.DOTALL):
                    args = {}
                    for line in g0.split('\n'):
                        m1 = re.match('^\|\s*([^=]+?)\s*=\s*(.*?)\s*$', line)
                        if m1:
                            args[m1.group(1).lower()] = m1.group(2)

                    if 'title' in args and 'coordinates' in args:
                        title = args['title'].replace('{{PAGENAME}}', response['title'])

                        found_carto_template = False
                        for server, carto_data in re.findall('\{\{Carto([CSP])\|?([^}]+)\}\}', args['coordinates']):
                            if server == 'C':
                                server = 'creative'
                            elif server == 'S':
                                server = 'survival'
                            elif server == 'P':
                                server = 'pve'
                            found_carto_template = True
                            carto_data = dict((d.split('=') for d in carto_data.split("|")))
                            if 'r' in carto_data \
                                    and 'x' in carto_data \
                                    and 'z' in carto_data:
                                #print "adding"
                                self._update_creation(
                                    title,
                                    server,
                                    int(carto_data['r']),
                                    int(carto_data['x']),
                                    int(carto_data['z'])
                            )
                        if not found_carto_template:

                            try:
                                revision = int(args.get('map_revision', None))
                            except:
                                revision = 0

                            server = args.get('server', '')\
                                .replace('[', '')\
                                .replace(']', '')\
                                .lower()

                            if server in ('creative', 'survival', 'pve', 'c', 's', 'p'):
                                if server == 'c':
                                    server = 'creative'
                                elif server == 's':
                                    server = 'survival'
                                elif server == 'p':
                                    server = 'pve'
                                else:
                                    server = server[0]
                            else:
                                server = 'unknown'

                            coords = re.findall('-?\d+', args['coordinates'])

                            # pop y coord
                            if len(coords) == 3:
                                coords.pop(1)

                            if len(coords) == 2:
                                coords = (int(coords[0]), int(coords[1]))
                            else:
                                coords = [0,0]

                            if revision and server and coords:
                                self._update_creation(
                                    title,
                                    server,
                                    revision,
                                    coords[0],
                                    coords[1]
                                )

        pp_content = 50

        while len(pages):
            pages_current, pages = pages[:pp_content], pages[pp_content:]
            d = self._get_text(None, *pages_current)
            d.addCallback(_callback)


    """def _handle_servers(self, result_list):
        for success, result in result_list:
            request_data, response_data = result
            html = response_data['parse']['text']['*']
            print "="*50
            print request_data['page']
            print html.encode('utf8')

        #import pprint
        #pprint.pprint(result)"""

source = WikiSource
