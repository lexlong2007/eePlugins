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

class MSNWeatherThingSpeak(Converter, object):
    def __init__(self, type):
        Converter.__init__(self, type)
        self.mode = type
        self.ThingSpeakItems = {}

    def syncItems(self):
        try:
            ThingSpeakItems = self.source.getThingSpeakItems()
        except Exception as e:
            if DBG: printDEBUG('\t','Exception %s' % str(e))
            return ''
        if len(ThingSpeakItems) > 0:
            self.ThingSpeakItems = ThingSpeakItems
    
    @cached
    def getText(self): #self.mode = ('name','description','field1Name','field2Name','ObservationTime','field1Value','field1Status','field2Value','field2Status')
        if DBG: printDEBUG('MSNWeatherThingSpeak:getText','>>> self.mode="%s"' % self.mode)
        self.syncItems()
        retTXT = ''
        if len(self.ThingSpeakItems) > 0:
            if self.mode == 'field1txt': retTXT = '%s %s:' %( self.ThingSpeakItems.get('field1Name', _("f1")), self.ThingSpeakItems.get('field1Value', '') )
            elif self.mode == 'field2txt': retTXT = '%s %s:' %( self.ThingSpeakItems.get('field2Name', _("f2")), self.ThingSpeakItems.get('field2Value', '') )
            else: retTXT = str(self.ThingSpeakItems.get(self.mode, ''))
        return retTXT
        
    text = property(getText)
    
    @cached
    def getIconFilename(self):
        if DBG: printDEBUG('MSNWeatherThingSpeak:getIconFilename','>>> self.mode="%s"' % self.mode)
        self.syncItems()
        return ""
            
    iconfilename = property(getIconFilename)
