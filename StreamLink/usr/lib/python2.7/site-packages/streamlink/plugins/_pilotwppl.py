# -*- coding: utf-8 -*-
import logging
import re

#from streamlink.compat import html_unescape
from streamlink.plugin import Plugin
from streamlink.plugin.api import useragents
#from streamlink.plugin.api.utils import itertags
from streamlink.stream import HLSStream
from streamlink.utils import update_scheme

log = logging.getLogger(__name__)

import sys
sys.path.append('/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/')

from wpConfig import headers
from wpConfig import params #'login_url', 'main_url', 'video_url', 'close_stream_url'
from wpConfig import data
from wpConfig import getCookie
from wpBouquet import _login

class PilotWPpl(Plugin):
    _url_re = re.compile(r"https?://pilot.wp.pl/api/v1/channel/")

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url) is not None

    def _get_streams(self):
        cookies = getCookie()
        if not cookies:
            cookies = _login()
          
        data = {'format_id': '2', 'device_type': 'android'}
        
        #print headers
        self.session.http.headers.update({'user-agent': headers['user-agent']})
        self.session.http.headers.update({'accept': headers['accept']})
        self.session.http.headers.update({'x-version': headers['x-version']})
        self.session.http.headers.update({'content-type': headers['content-type']})
        self.session.http.headers.update({'Cookie': cookies})
        response = self.session.http.get(
                self.url,
                params=data,
                verify=False,
                headers=headers,
            ).json()
        
        log.debug("Response: %s" % response)
        meta = response.get('_meta', None)
        log.debug("meta: %s" % meta)
        if meta is not None:
            token = meta.get('error', {}).get('info', {}).get('stream_token', None)
            log.debug("token: %s" % token)
            """if token is not None:
                json = {'channelId': video_id, 't': token}
                response = requests.post(
                    close_stream_url,
                    json=json,
                    verify=False,
                    headers=headers
                  ).json()
                if response.get('data', {}).get('status', '') == 'ok' and not retry:
                    return stream_url(video_id, True)
                else:
                    return"""
            
        if 'hls@live:abr' in response[u'data'][u'stream_channel'][u'streams'][0][u'type']:
            type = 'hls'
            finalUrl = response[u'data'][u'stream_channel'][u'streams'][0][u'url'][0]
        else:
            type = 'not hls'
            finalUrl = response[u'data'][u'stream_channel'][u'streams'][1][u'url'][0]
            
            return HLSStream.parse_variant_playlist(
                self.session,
                update_scheme(self.url, finalUrl),
                headers={'Referer': self.url, 
                         'user-agent': headers['user-agent'],
#                         'accept': 'application/json', 
                         'x-version': headers['x-version'],
#                         'content-type': 'application/json; charset=UTF-8',
                         'Cookie': cookies}
            ) 

__plugin__ = PilotWPpl
