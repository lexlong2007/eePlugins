# -*- coding: utf-8 -*-
#
# j00zek 2018/2019
#

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Language import language

#simple and dirty translation
if language.getLanguage() == 'pl_PL':
    translationsDict = {'Support for skin:': 'Wsparcie:', 'Flash Free:': 'Wolne:',
                        'Load Avg:': 'Obciążenie CPU:', 'Uptime:': 'Czas pracy:', 'Memory:': 'Pamięć RAM:', 'Box Type:': 'Typ tunera:', 'Flash:': 'Pamięć Flash:',
                        'Flash Free:': 'Wolne:', 'Show Maps': 'Mapy','Show Histograms': 'Histogramy',
                        'Playing since:': 'Gramy od:'}
else:
    translationsDict = {} 
    
class j00zekTranslator(Converter, object):
    def __init__(self, LabelText):
        Converter.__init__(self, LabelText)
        LabelText = _(LabelText) #first translation using enigma2.po
        self.translatedLabel = translationsDict.get(LabelText, LabelText) #second own translation, if exists

    @cached
    def getText(self):
        return self.translatedLabel
        
    text = property(getText)
