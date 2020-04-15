import logging
import re

from streamlink.compat import html_unescape
from streamlink.plugin import Plugin
from streamlink.plugin.api import useragents
from streamlink.plugin.api.utils import itertags

log = logging.getLogger(__name__)

import sys
sys.path.append('/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/')
from wpConfig import *

class PilotWPpl(Plugin):
    _url_re = re.compile(r"https?://pilot.wp.pl/api/v1/channel/")

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url) is not None

    def _get_streams(self):
        #if not sessionid:
        login()
        cookies = readFromDB()
        #print sessionid    
        print cookies
        data = {'format_id': '2', 'device_type': 'android'}
        
        #print headers
        self.session.http.headers.update({'user-agent': 'ExoMedia 4.3.0 (43000) / Android 8.0.0 / foster_e'})
        self.session.http.headers.update({'accept': 'application/json'})
        self.session.http.headers.update({'x-version': 'pl.videostar|3.25.0|Android|26|foster_e'})
        self.session.http.headers.update({'content-type': 'application/json; charset=UTF-8'})
        self.session.http.headers.update({'Cookie': cookies})
        response = self.session.http.get(
                self.url,
                params=data,
                verify=False,
                headers=headers,
            ).json()
        
        print 'Response:', response
        meta = response.get('_meta', None)
        print 'meta:', meta
        if meta is not None:
            token = meta.get('error', {}).get('info', {}).get('stream_token', None)
            print 'token', token
            
        print 'type', response[u'data'][u'stream_channel'][u'streams'][0][u'type']
        if 'hls@live:abr' in response[u'data'][u'stream_channel'][u'streams'][0][u'type']:
            print 'type', response[u'data'][u'stream_channel'][u'streams'][0][u'url'][0]
            return self.session.streams(response[u'data'][u'stream_channel'][u'streams'][0][u'url'][0])
        else:
            print 'type', response[u'data'][u'stream_channel'][u'streams'][1][u'url'][0]
            return self.session.streams(response[u'data'][u'stream_channel'][u'streams'][1][u'url'][0])


__plugin__ = PilotWPpl
