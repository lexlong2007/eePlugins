# -*- coding: utf-8 -*-
#  
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Language import language

#simple and dirty translation
if language.getLanguage() == 'pl_PL':
    translationsDict = {'Support for skin:': 'Wsparcie:', 'http://forum.dvhk.pl': 'http://forum.dvhk.to', 'Flash Free:': 'Wolne:',
                        'Load Avg:': 'Obciążenie CPU:', 'Uptime:': 'Czas pracy:', 'Memory:': 'Pamięć RAM:', 'Box Type:': 'Typ tunera:', 'Flash:': 'Pamięć Flash:',
                        'Flash Free:': 'Wolne:'}
else:
    translationsDict = {} 
    
class j00zekTranslator(Converter, object):
    def __init__(self, LabelText):
        Converter.__init__(self, LabelText)
        self.translatedLabel = translationsDict.get(LabelText, LabelText)

    @cached
    def getText(self):
        return self.translatedLabel
        
    text = property(getText)
