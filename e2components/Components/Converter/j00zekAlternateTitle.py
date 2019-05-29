# -*- coding: utf-8 -*-
#  
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Language import language

#simple and dirty translation
if language.getLanguage() == 'pl_PL':
    translationsDict = {'Timer Edit List': 'Lista timerów',
                        }
else:
    translationsDict = {} 
    
class j00zekAlternateTitle(Converter, object):
    def __init__(self, LabelText):
        Converter.__init__(self, LabelText)
        self.translatedLabel = translationsDict.get(LabelText, LabelText)

    @cached
    def getText(self):
        retText = ''
        try:
            retText = str(self.source.text)
        except Exception as e:
            retText = self.translatedLabel
            import os
            os.system("echo '[j00zekAlternateTitle] exception %s' >> /tmp/j00zekComponents.log.log" % str(e))
        if len(retText) < 5:
            retText = self.translatedLabel
        return retText
        
    text = property(getText)
