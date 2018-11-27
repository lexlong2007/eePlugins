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

DBG = False

class MSNWeatherWebCurrent(Converter, object):
    def __init__(self, type):
        if DBG: printDEBUG('MSNWeatherWebCurrent','__init__')
        Converter.__init__(self, type)
        self.mode = type
        self.WebCurrentItems = {}

    def syncItems(self):
        try:
            WebCurrentItems = self.source.getWebCurrentItems()
        except Exception as e:
            if DBG: printDEBUG('\t','Exception %s' % str(e))
        if len(WebCurrentItems) > 0:
            self.WebCurrentItems = WebCurrentItems
    
    @cached
    def getText(self): #self.mode = ('name','description','field1Name','field2Name','ObservationTime','field1Value','field1Status','field2Value','field2Status')
        if DBG: printDEBUG('MSNWeatherWebCurrent:getText','>>> self.mode="%s"' % self.mode)
        self.syncItems()
        retTXT = '?'
        if DBG: printDEBUG('','######\n%s\n#####' % self.WebCurrentItems)
        if len(self.WebCurrentItems) > 0:
            try:
                for line in self.WebCurrentItems.get('nowData', []):
                    if line[0].lower() == self.mode.lower() and self.mode.lower() == 'barometr':
                        retTXT = str('Ciœnienie %s' % (line[1].strip()))
                    elif line[0].lower() == self.mode.lower(): #available: 'Temperatura odczuwalna','Wiatr','Barometr','Widoczno\xc5\x9b\xc4\x87','Wilgotno\xc5\x9b\xc4\x87','Temperatura punktu rosy'
                        retTXT = str('%s: %s' % (line[0].strip(), line[1].strip()))
            except Exception as e:
                if DBG: printDEBUG('\t','Exception %s' % str(e))
        if DBG: printDEBUG('\t','retTXT=%s' % retTXT)
        return retTXT
        
    text = property(getText)
    
    @cached
    def getIconFilename(self):
        if DBG: printDEBUG('MSNWeatherWebCurrent:getIconFilename','>>> self.mode="%s"' % self.mode)
        self.syncItems()
        return ""
            
    iconfilename = property(getIconFilename)
