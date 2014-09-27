import json
import re

from twisted.internet import defer, task
from twisted.web import client
client.HTTPClientFactory.noisy = False

from sources import Source


class StaffSource(Source):

    def start(self):
        task.LoopingCall(self.update).start(60*60*2)

    def update(self):
        d = client.getPage('http://nerd.nu/staff')
        d.addCallback(self._handle_staff)

    def _handle_staff(self, response_data):
        staff = {}

        # Strip linebreaks and excessive whitespace
        response_data = re.sub('[\r\n\t ]+', ' ', response_data)

        # Grab sections
        # We actually grab the title of the next section, so we have to swap
        #   at the end of each iteration
        title = None
        for section, level, new_title in re.findall('(.*?)<h([0-9]).*?>([^<]+)', response_data):
            if title:
                # In Memoriam section returns players as a dictionary
                if title == "In Memoriam":
                    players = dict(re.findall('&p=(.*?)".*?clear: both">(.*?)\s*<', section))

                # Otherwise use a list
                else:
                    players = re.findall('&p=(.*?)"', section)

                if players:
                    staff[title] = players

            if level == "2":
                title = new_title
            elif level == "3":
                title = "%s Admins" % new_title
            else:
                title = None


        staff = json.dumps(staff)
        self.api_call("update_cache", key="STAFF_LIST", value=staff)


source = StaffSource
