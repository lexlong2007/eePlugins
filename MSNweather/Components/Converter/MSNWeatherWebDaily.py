# -*- coding: utf-8 -*-
#######################################################################
#
#    MSNweather extension Converter for Enigma2
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
####################################################################### 

from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eTimer
from Plugins.Extensions.WeatherPlugin.debug import printDEBUG
from Plugins.Extensions.WeatherPlugin.__init__ import _
import os
import datetime

DBG = False
DBGText = False
DBGIcons = False

iconsMap={
    '1' : '29.png', #zachmurzenie ma³e
    '2' : '30.png', #Czêœciowo s³onecznie
    'BBih5H' : '32.png', #S³onecznie
    '4' : '34.png', #Przewa¿nie s³onecznie
    }

class MSNWeatherWebDaily(Converter, object):
    def __init__(self, type):
        if DBG: printDEBUG('MSNWeatherWebDaily','__init__')
        Converter.__init__(self, type)
        self.mode = type
        self.WebDailyItems = {}
        self.path = '/usr/lib/enigma2/python/Plugins/Extensions/WeatherPlugin/icons'

    def syncItems(self):
        try:
            WebDailyItems = self.source.getWebDailyItems()
        except Exception as e:
            if DBG: printDEBUG('\t','Exception %s' % str(e))
        if len(WebDailyItems) > 0:
            self.WebDailyItems = WebDailyItems
    
    @cached
    def getText(self):
        if DBGText: printDEBUG('MSNWeatherWebDaily:getText','>>> self.mode="%s"' % self.mode)
        self.syncItems()
        retTXT = '?'
        #if DBG: printDEBUG('','######\n%s\n#####' % self.WebDailyItems)
        if len(self.WebDailyItems) > 0:
            try:
                mode = self.mode.split(',')
                if DBGText: printDEBUG('\t','len(mode) =%s' % str(len(mode)))
                if len(mode) >= 2:
                    record = mode[0]
                    day = int(record.split('=')[1])
                    Month = _((datetime.date.today() + datetime.timedelta(days=day)).strftime("%b"))
                    item =  mode[1]
                    line = self.WebDailyItems.get(record, [('', '', '', '', '')])
                    line = line[0]
                    if item ==  'date':
                        retTXT = str('%s. %s %s' % (line[1].strip().lower(), line[2].strip(), Month))
                    elif item ==  'info':
                        retTXT = str('%s %s %s\n%s' % (line[6].strip(), line[7].strip(), line[8].strip(), line[4].strip()))
            except Exception as e:
                if DBGText: printDEBUG('\t','Exception %s' % str(e))
        if DBGText: printDEBUG('\t','retTXT=%s' % retTXT)
        return retTXT
        
    text = property(getText)
    
    @cached
    def getIconFilename(self):
        if DBGIcons: printDEBUG('MSNWeatherWebDaily:getIconFilename','>>> self.mode="%s"' % self.mode)
        self.syncItems()
        iconFileName = 'fake.png'
        if len(self.WebDailyItems) > 0:
            try:
                line = self.WebDailyItems.get(self.mode, [('', '', '', '', '')])
                line = line[0]
                url = str('%s' % line[3].strip())
                if DBGIcons: printDEBUG('MSNWeatherWebDaily:getIconFilename','url=%s' % url)
                icon = '%s' % (url.split('?')[0].split('/')[-1][:-4])
                iconpng = iconsMap.get(icon, icon)
                if icon == iconpng: #no mapping exists
                    iconFileName = '%s/%s.png' % (self.path, icon)
                    if not os.path.exists(iconFileName):
                        import urllib
                        if 'url'[:4] != 'http': url = 'http:' + url
                        if DBGIcons: printDEBUG('MSNWeatherWebDaily:getIconFilename','downloading %s' % url)
                        urllib.urlretrieve(url, iconFileName)
                else:
                    if DBGIcons: printDEBUG('MSNWeatherWebDaily:getIconFilename','icon %s translated to %s' % (icon,iconpng))
                    iconFileName = '/usr/share/enigma2/BlackHarmony/weather_icons/%s' % (iconpng)
            except Exception as e:
                if DBGIcons: printDEBUG('MSNWeatherWebDaily:getIconFilename','Exception %s' % str(e))
        if DBGIcons: printDEBUG('MSNWeatherWebDaily:getIconFilename','iconFileName=%s' % iconFileName)
        return iconFileName
            
    iconfilename = property(getIconFilename)
