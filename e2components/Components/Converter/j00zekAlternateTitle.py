# -*- coding: utf-8 -*-
#
# j00zek 2019/2020
# some images doesn't present title, some doesn't translate
# this converter is to manage over this situations
#

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.j00zekSkinTranslatedLabels import translate
    
class j00zekAlternateTitle(Converter, object):
    def __init__(self, LabelText):
        Converter.__init__(self, LabelText)
        self.translatedLabel = translate(LabelText)

    @cached
    def getText(self):
        retText = ''
        try:
            retText = translate(str(self.source.text))
        except Exception as e:
            retText = self.translatedLabel
        if len(retText) < 5:
            retText = self.translatedLabel
        return retText
        
    text = property(getText)
