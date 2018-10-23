# -*- coding: utf-8 -*-
#######################################################################
#
#    Converter for Enigma2
#    Coded by j00zek (c)2018
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem konwertera
#    Please respect my work and don't delete/change name of the converter author
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#     
# To display text (e.g. movie title):
# <widget font="Regular;22" foregroundColor="white" position="10,10" render="Label" size="315,24" source="global.CurrentTime" transparent="1" zPosition="5">
#    <convert type="j00zekLCD4KODI">title</convert>
# </widget> 
#
# Parameters:
#       kodistate: returns
#
#######################################################################

from enigma import eTimer
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Language import language
from Poll import Poll 
from datetime import timedelta

#if enabled log into /tmp/e2components.log
DBG = True
if DBG: from Components.j00zekComponents import j00zekDEBUG

from Components.j00zekKodistate import remoteKODI, AppProperties, XBMCInfoBool, GetActivePlayers, \
                                        AudioPlayerState, VideoPlayerState, VideoPlayerTime
try:
    from Components.config import config
    KODI_IP = config.plugins.ShareLCDwithKODI.IP.value
    KODI_IP = '%s.%s.%s.%s' % (KODI_IP[0],KODI_IP[1],KODI_IP[2],KODI_IP[3])
    KODI_PORT = config.plugins.ShareLCDwithKODI.PORT.value
    if DBG: j00zekDEBUG('[j00zekLCD4KODI] using config from ShareLCDwithKODI plugin: %s:%s' %(KODI_IP,KODI_PORT))
except Exception:
    if DBG: j00zekDEBUG('[j00zekLCD4KODI] using config from j00zekKodistate: %s:%s' %(KODI_IP,KODI_PORT))
    from Components.j00zekKodistate import KODI_IP, KODI_PORT

#simple and dirty translation
if language.getLanguage() == 'pl_PL':
    translationsDict = {'is off': 'wyłączone', 'is sleeping': 'uśpione', 'is on': 'włączone', 'is playing': 'odtwarza'}
else:
    translationsDict = {}

def _(text):
    return translationsDict.get(text,text)
        
#STATE global TABLE
statesDefRable = {'powerOn': False,
                  'isIdle': True,
                  'isPlaying': False,
                  'state': '',
                  'name': 'KODI',
                  'version': '',
                  'activePlayerID': -1,
                  'activePlayerType': 'unknown',
                  'title': '',
                  'duration': 0,
                  'progress': 0
                 }
KODIstateTable = statesDefRable

class j00zekLCD4KODI(Poll, Converter, object):
    UNKNOWN = 0
    FULLINFO = 1
    NAME = 2
    VERSION = 3
    STATE = 4
    TITLE = 5
    DURATION = 6
    PROGRESS = 7
    STATEICON = 8
    PLAYEDTIME = 9
    LEFTTIME = 10
    LEFTMINS = 11
    
    def __init__(self, arg):
        Converter.__init__(self, arg)
        Poll.__init__(self)
        if DBG: j00zekDEBUG('[j00zekLCD4KODI:__init__] >>>')
        self.kodi = remoteKODI(KODI_IP, KODI_PORT) 
        self.running = False
        self.isSuspended = False
        if arg in ('fullInfo','kodinameversionstate'): self.requested = self.FULLINFO
        elif arg == 'name': self.requested = self.NAME
        elif arg == 'version': self.requested = self.VERSION
        elif arg == 'state': self.requested = self.STATE
        elif arg == 'title': self.requested = self.TITLE
        elif arg == 'duration': self.requested = self.DURATION
        elif arg == 'progress': self.requested = self.PROGRESS
        elif arg == 'stateicon': self.requested = self.STATEICON
        elif arg == 'playedtime': self.requested = self.PLAYEDTIME
        elif arg == 'lefttime': self.requested = self.LEFTTIME
        elif arg == 'leftmins': self.requested = self.LEFTMINS
        else: self.requested = self.UNKNOWN
        
        self.poll_interval = 1000 
        self.poll_enabled = True

    def doSuspend(self, suspended): 
        if DBG: j00zekDEBUG('[j00zekLCD4KODI] doSuspend(%s) >>> ' % suspended)
        if suspended == 1: 
            self.poll_enabled = False 
            self.isSuspended = True
        else: 
            self.poll_enabled = True 
            self.isSuspended = False

    def changed(self, what):
        global KODIstateTable
        prevState = KODIstateTable
        if what[0] == self.CHANGED_POLL and not self.isSuspended and not self.running:
            self.running = True
            self.checkState()
            self.running = False
            if DBG: j00zekDEBUG("[j00zekLCD4KODI:getText] changed=")
            self.downstream_elements.changed(what) 

    def resetKODIstateTable(self):
        global KODIstateTable, statesDefRable
        KODIstateTable = statesDefRable
        self.poll_interval = 30000 #check state once a 30s when Kodi not running
    
    @cached
    def getValue(self):
        val = 0
        global KODIstateTable
        if not KODIstateTable['isPlaying']:
            val = 0
        elif self.requested == self.PROGRESS:
            val = KODIstateTable['progress']
        if DBG: j00zekDEBUG("[j00zekLCD4KODI:getText] self.requested=%s, val='%s'" % (self.requested, val))
        return int(val)

    value = property(getValue)
    range = 100 

    @cached
    def getText(self):
        global KODIstateTable
        retTXT = ''
        try:
            if self.requested == self.FULLINFO:
                retTXT = '%s %s %s %s' %( KODIstateTable['name'],
                                          KODIstateTable['version'],
                                          _(KODIstateTable['state']),
                                          KODIstateTable['title']
                                        )
            elif self.requested == self.STATEICON:
                if not KODIstateTable['powerOn']: retTXT = 'off'
                elif KODIstateTable['isIdle']: retTXT = 'sleep'
                elif KODIstateTable['isPlaying']: retTXT = 'play'
                else: retTXT = 'on'
            elif not KODIstateTable['isPlaying']:
                retTXT = ''
            elif self.requested == self.TITLE:  
                retTXT = KODIstateTable['title']
            elif self.requested == self.DURATION:
                retTXT = str(timedelta(seconds=KODIstateTable['duration']))
            elif self.requested == self.PLAYEDTIME:
                p = int(KODIstateTable['duration'] * (KODIstateTable['progress'] /100))
                retTXT = str(timedelta(seconds=p))
            elif self.requested == self.LEFTTIME:
                p = int(KODIstateTable['duration'] - (KODIstateTable['duration'] * (KODIstateTable['progress'] /100)))
                retTXT = str(timedelta(seconds=p))
            elif self.requested == self.LEFTMINS:
                p = int(KODIstateTable['duration'] - (KODIstateTable['duration'] * (KODIstateTable['progress'] /100)))
                retTXT = '+ %s min' % int(p/60)
            
        except Exception as e:
            if DBG: j00zekDEBUG("[j00zekLCD4KODI:getText] Exception='%s'" % str(e))
            retTXT = '??'
        if DBG: j00zekDEBUG("[j00zekLCD4KODI:getText] self.requested=%s, retTXT='%s'" % (self.requested, str(retTXT).strip()))
        return str(retTXT).strip()

    text = property(getText)
    
    def getData(self, request):
        if DBG: j00zekDEBUG("[j00zekLCD4KODI:getData] request = '%s'" %  str(request))
        response = self.kodi.getState(request)
        if DBG: j00zekDEBUG('[j00zekLCD4KODI:getData] response=%s' % response)
        return response
    
    def checkState(self):
        if DBG: j00zekDEBUG('[j00zekLCD4KODI:checkState] >>>')
        global KODIstateTable
        try:
            ########## step1: check if kodi is running ########## 
            response = self.getData(AppProperties)
            if response.get('isError',True):
                self.resetKODIstateTable()
                return
            else: 
                KODIstateTable['powerOn'] = True
                KODIstateTable['name'] = response.get('name','KODI')
                KODIstateTable['version'] = "%s.%s" % (response['version']['major'], response['version']['minor'])
            ########## step2: check if kodi is my sleeping ########## 
            self.poll_interval = 10000 #check state once a 10s when Kodi is running
            response = self.getData(XBMCInfoBool)
            if response.get('isError',True):
                self.resetKODIstateTable()
                return
            elif response.get('System.ScreenSaverActive ',False):
                KODIstateTable['isIdle'] = True
                KODIstateTable['state'] = 'is sleeping'
                return
            else:
                KODIstateTable['state'] = 'is on'
                KODIstateTable['isIdle'] = False
            ########## step3: check if kodi is playing ########## 
            response = self.getData(GetActivePlayers)
            if response.get('isError',True):
                self.resetKODIstateTable()
                return
            elif response.get('playerid', -1) == -1:
                KODIstateTable['isPlaying'] = False
                return
            else:
                KODIstateTable['activePlayerID'] = response.get('playerid', -1)
                KODIstateTable['activePlayerType'] = response.get('type', 'unknown')
                KODIstateTable['state'] = 'is playing'
                KODIstateTable['isPlaying'] = True
            ########## step4: get data for active player ##########
            if KODIstateTable['activePlayerID'] == 0: #audio
                response = self.getData(AudioPlayerState)
            elif KODIstateTable['activePlayerID'] == 1: #video
                response = self.getData(VideoPlayerState)
                if response.get('isError',True):
                    return
                else:
                    if response['item']['showtitle'] != '': KODIstateTable['title'] = response['item']['showtitle']
                    elif response['item']['title'] != '': KODIstateTable['title'] = response['item']['title']
                    if response['item']['label'] != '': KODIstateTable['title'] = response['item']['label']
                    else: KODIstateTable['title'] = response['item']['file']
                    KODIstateTable['duration'] = int(response['item']['streamdetails']['video'][0]['duration'])
                response = self.getData(VideoPlayerTime)
                if response.get('isError',True):
                    return
                else:
                    KODIstateTable['progress'] = float(response['percentage'])
        except Exception, e:
            if DBG: j00zekDEBUG("[j00zekLCD4KODI:checkState] Exception = '%s'" %  str(e))
        if DBG: j00zekDEBUG('[j00zekLCD4KODI:checkState] <<<')
        return
