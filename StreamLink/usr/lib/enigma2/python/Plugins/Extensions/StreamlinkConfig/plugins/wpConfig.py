# -*- coding: utf-8 -*-
#
#   Based on Kodi plugin.video.pilot.wp by c0d34fun
#   Coded by j00zek
#
from streamlink.e2config import getE2config

import sys
import os
from urlparse import parse_qsl
import urllib
import requests
import emukodi.xbmc as xbmc
import emukodi.xbmcgui as xbmcgui
import emukodi.xbmcplugin as xbmcplugin
import emukodi.xbmcaddon as xbmcaddon
import emukodi.xbmcvfs as xbmcvfs

#constants
base_url = '' #sys.argv[0]
addon_handle = 0 #int(sys.argv[1])
params = {} #dict(parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.pilot.wp')

login_url = 'https://pilot.wp.pl/api/v1/user_auth/login'
main_url = 'https://pilot.wp.pl/api/v1/channels/list?device=androidtv'
video_url = 'https://pilot.wp.pl/api/v1/channel/'
close_stream_url = 'https://pilot.wp.pl/api/v1/channels/close'

headers = {
    'user-agent': 'ExoMedia 4.3.0 (43000) / Android 8.0.0 / foster_e',
    'accept': 'application/json',
    'x-version': 'pl.videostar|3.25.0|Android|26|foster_e',
    'content-type': 'application/json; charset=UTF-8'
}

username = addon.getSetting('username')
password = addon.getSetting('password')
file_name = addon.getSetting('fname')
path = addon.getSetting('path')
sessionid = params.get('sessionid', '')

#addonInfo = xbmcaddon.Addon().getAddonInfo
dataPath = '/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig' #xbmc.translatePath(addonInfo('profile')).decode('utf-8')
cacheFile = os.path.join(dataPath, 'WPConfigCache.db')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def add_item(name, image, is_folder, is_playble, payload, plot=''):
    list_item = xbmcgui.ListItem(label=name)

    if is_playble:
        list_item.setProperty("IsPlayable", 'true')
    else:
        list_item.setProperty("IsPlayable", 'false')

    list_item.setInfo(type='video', infoLabels={
                      'title': name, 'sorttitle': name, 'plot': plot})
    list_item.setArt({'thumb': image, 'poster': image, 'banner': image})
    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=build_url(payload),
        listitem=list_item,
        isFolder=is_folder
    )


def saveToDB(table_name, value):
    import sqlite3
    import os
    if os.path.exists(cacheFile):
        os.remove(cacheFile)
    else:
        print('File does not exists')
    conn = sqlite3.connect(cacheFile, detect_types=sqlite3.PARSE_DECLTYPES,
                           cached_statements=20000)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Cache(%s TEXT)' % table_name)
    c.execute("INSERT INTO Cache('%s') VALUES ('%s')" % (table_name, value))
    conn.commit()
    c.close()

def readFromDB():
    import sqlite3
    conn = sqlite3.connect(cacheFile, detect_types=sqlite3.PARSE_DECLTYPES,
                           cached_statements=20000)
    c = conn.cursor()
    c.execute("SELECT * FROM Cache")
    for row in c:
        if row:
            c.close()
            return row[0]

def cookiesToString(cookies):
    try:
        return "; ".join([str(x) + "=" + str(y) for x, y in cookies.get_dict().items()])
    except Exception as e:
        print (e)
        return ''

def login():
    if len(password) > 0 and len(username) > 0:
        data = {'device': 'AndroidTV', 'login': username, 'password': password}

        response = requests.post(
            login_url,
            json=data,
            verify=False,
            headers=headers
        )

        meta = response.json().get('_meta', None)
        if meta is not None:
            if meta.get('error', {}).get('name', None) is not None:
                xbmcgui.Dialog().notification('Nieudane logowanie', 'Sprawdź login i hasło w ustawieniach wtyczki.',
                                              xbmcgui.NOTIFICATION_ERROR, 5000)
                return ''

        saveToDB('wppilot_cache', cookiesToString(response.cookies))
        return cookiesToString(response.cookies)

    else:
        xbmcgui.Dialog().notification('Nieudane logowanie', 'Sprawdź login i hasło w ustawieniach wtyczki.',
                                      xbmcgui.NOTIFICATION_ERROR, 5000)
        return ''

def generate_m3u():
    if not sessionid:
        return

    if file_name == '' or path == '':
        xbmcgui.Dialog().notification('WP Pilot', 'Ustaw nazwe pliku oraz katalog docelowy.',
                                      xbmcgui.NOTIFICATION_ERROR)
        return

    xbmcgui.Dialog().notification('WP Pilot', 'Generuje liste M3U.',
                                  xbmcgui.NOTIFICATION_INFO)
    data = '#EXTM3U\n'

    for item in channels():
        if item.get('access_status', '') != 'unsubscribed':
            id = item.get('id', None)
            title = item.get('name', '')
            data += '#EXTINF:-1,%s\nplugin://plugin.video.pilot.wp?action=PLAY&channel=%s\n' % (
                title, id)

    f = xbmcvfs.File(path + file_name, 'w')
    f.write(data.encode('utf-8'))
    f.close()

    xbmcgui.Dialog().notification('WP Pilot', 'Wygenerowano liste M3U.', xbmcgui.NOTIFICATION_INFO)

if __name__ == '__main__' and len(sys.argv) >=5:
    global username, password, file_name, sessionid
    username = sys.argv[1]
    password = sys.argv[2]
    file_name = sys.argv[3]
    streamlinkURL = 'http%3a//127.0.0.1%3a%s/' % sys.argv[4]
    if not sessionid or sessionid == '':
        sessionid = login()
    generate_m3u() 