import re

from twisted.internet import task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from sources import Source


class ModreqSource(Source):

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        for server in ('creative', 'pve'):
            d = client.getPage('http://nerd.nu/modreq/%s.pl' % server)
            d.addCallback(self._handle_modreqs, server)

    def _handle_modreqs(self, response_data, server):
        columns = [
            'id',
            'request_by',
            'request_text',
            'status',
            'response_by',
            'response_text'
        ]
        rows = []
        for row_html in re.findall('<tr.*?><td>(.*?)</td></tr>', response_data):
            row_parts = row_html.split("</td><td>")
            row_data = dict(zip(columns, row_parts))
            row_data['server'] = server
            self.api_call('update_modreq', **row_data)


source = ModreqSource
