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
from Plugins.Extensions.WeatherPlugin.__init__ import _
import os
import datetime

DBG = False
DBGText = False
DBGIcons = True
if DBG or DBGText or DBGIcons:
    from Plugins.Extensions.WeatherPlugin.debug import printDEBUG

iconsMap={
    '0'         :  '0.png', #
    '1'         :  '1.png', #
    '2'         :  '2.png', #
    '3'         :  '3.png', #
    '4'         :  '4.png', #
    '5'         :  '5.png', #
    'BBi9D1'    :  '6.png', #Lekki deszcz ze śniegiem
    '7'         :  '7.png', #
    '8'         :  '8.png', #
    'BBi9ul'    :  '9.png', #Slabe opady deszczu
    '10'        : '10.png', #
    'BB1kvFq'   : '11.png', #Opady deszczu
    '12'        : '12.png', #
    'BBiAZc'    : '13.png', #Niewielkie opady śniegu 
    '14'        : '14.png', #
    '15'        : '15.png', #
    '16'        : '16.png', #Śnieg
    '17'        : '17.png', #
    '18'        : '18.png', #
    '19'        : '19.png', #
    '20'        : '20.png', #
    '21'        : '21.png', #
    '22'        : '22.png', #
    '23'        : '23.png', #
    '24'        : '24.png', #
    '25'        : '25.png', #
    'BBaGxJ'    : '26.png', #Zachmurzenie calkowite
    'BB1kc8s'   : '26.png', #Zachmurzenie calkowite
    '27'        : '27.png', #Zachmurzenie duże
    '28'        : '28.png', #Zachmurzenie duze
    '29'        : '29.png', #zachmurzenie male
    'BB1kvzy'   : '30.png', #Czesciowo slonecznie
    '31'        : '31.png', #Bezchmurnie - slonce
    'BBih5H'    : '32.png', #Slonecznie
    '33'        : '33.png', #
    'BBb3WX'    : '34.png', #Przewaznie slonecznie
    '35'        : '35.png', #
    '36'        : '36.png', #
    '37'        : '37.png', #
    '38'        : '38.png', #
    '39'        : '39.png', #
    '40'        : '40.png', #
    '41'        : '41.png', #
    '42'        : '42.png', #
    '43'        : '43.png', #
    '44'        : '44.png', #
    '45'        : '45.png', #
    '46'        : '46.png', #
    '47'        : '47.png', #
    '48'        : '48.png', #
    }

class MSNWeatherWebDaily(Converter, object):
    def __init__(self, type):
        if DBG: printDEBUG('MSNWeatherWebDaily(Converter).__init__')
        Converter.__init__(self, type)
        self.mode = type
        self.WebDailyItems = {}
        self.path = '/usr/lib/enigma2/python/Plugins/Extensions/WeatherPlugin/icons'
            
    def syncItems(self):
        if DBG: printDEBUG('MSNWeatherWebDaily(Converter).syncItems >>>')
        self.WebDailyItems = self.source.getWebDailyItems().copy()
    
    @cached
    def getText(self):
        if DBG: printDEBUG('MSNWeatherWebDaily(Converter).getText >>> self.mode="%s"' % self.mode)
        self.syncItems()
        retTXT = ''
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
                        retTXT = str('%s/ %s/ %s\n%s' % (line[6].strip(), line[7].strip(), line[8].strip(), line[4].strip()))
            except Exception as e:
                if DBG: printDEBUG('\t','Exception %s' % str(e))
        if DBGText: printDEBUG('\t','retTXT="%s"' % retTXT)
        return retTXT
        
    text = property(getText)
    
    @cached
    def getIconFilename(self):
        if DBG: printDEBUG('MSNWeatherWebDaily(Converter).getIconFilename >>> self.mode="%s"' % self.mode)
        self.syncItems()
        iconFileName = 'fake.png'
        if len(self.WebDailyItems) > 0:
            try:
                line = self.WebDailyItems.get(self.mode, [('', '', '', '', '')])
                line = line[0]
                url = str('%s' % line[3].strip())
                if DBG: printDEBUG('MSNWeatherWebDaily(Converter).getIconFilename url=%s' % url)
                icon = '%s' % (url.split('?')[0].split('/')[-1][:-4])
                iconpng = iconsMap.get(icon, icon)
                if icon == iconpng: #no mapping exists
                    iconFileName = '%s/%s.png' % (self.path, icon)
                    if not os.path.exists(iconFileName):
                        import urllib
                        if 'url'[:4] != 'http': url = 'http:' + url
                        if DBG: printDEBUG('MSNWeatherWebDaily(Converter).getIconFilename downloading %s' % url)
                        urllib.urlretrieve(url, iconFileName)
                    if DBGIcons: printDEBUG('MSNWeatherWebDaily(Converter).getIconFilename NOT translated icon=%s, info=%s' % (iconFileName,line[4].strip()))
                else:
                    if DBG: printDEBUG('MSNWeatherWebDaily(Converter).getIconFilename icon %s translated to %s' % (icon,iconpng))
                    iconFileName = '/usr/share/enigma2/BlackHarmony/weather_icons/%s' % (iconpng)
            except Exception as e:
                if DBG: printDEBUG('MSNWeatherWebDaily(Converter).getIconFilename Exception %s' % str(e))
        if DBG: printDEBUG('MSNWeatherWebDaily(Converter).getIconFilenameiconFileName=%s, info=%s' % (iconFileName,line[4].strip()))
        return iconFileName
            
    iconfilename = property(getIconFilename)
