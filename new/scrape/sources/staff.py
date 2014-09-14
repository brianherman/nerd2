import json
import urllib
import math

from bs4 import BeautifulSoup
from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from sources import Source


class StaffSource(Source):

    def _query(self, **request_data):
        d0 = defer.Deferred()

        def _callback(d):
            d0.callback(BeautifulSoup(d.decode('utf8')))

        def _errback(e):
            d0.errback(e)

        url = 'http://nerd.nu/staff'

        d1 = client.getPage(url)
        d1.addCallbacks(_callback, _errback)

        return d0

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        d = self._query()
        d.addCallback(self._handle_staff)

    def _handle_staff(self, response_data):
        content = response_data

        staff = {}

        for role in content.find_all('h2'):
            name = role.string

            if name == 'Server Admins':
                h3s = role.find_all_next('h3')
                for h3 in h3s:
                    name = h3.string+' Admins'
                    ul = h3.find_next('ul', class_=["playerlist", "playerlist2"])

                    players = []

                    for li in ul.find_all('li'):
                        p = li.find('p')
                        player = p.string
                        players.append(player)

                    staff[name] = players

            elif name == 'In Memoriam':
                uls = role.find_all_next('ul', class_=["playerlist", "playerlist2"])

                players = {}

                for ul in uls:
                    li = ul.find('li')
                    p = li.find('p')
                    player = p.string

                    text = p.find_next('p').string

                    players[player] = text

                staff[name] = players

            else:
                ul = role.find_next('ul', class_=["playerlist", "playerlist2"])

                players = []

                for li in ul.find_all('li'):
                    p = li.find('p')
                    player = p.string
                    players.append(player)

                staff[name] = players


        staff = json.dumps(staff)
        self.api_call("update_cache", key="STAFF_LIST", value=staff)


source = StaffSource
