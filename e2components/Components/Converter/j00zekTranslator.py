# -*- coding: utf-8 -*-
#
# j00zek 2018/2019/2020
# eLabel is simple to use but not translated
# this converter is to use instead and have texts localized
#
#

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.j00zekSkinTranslatedLabels import translate

class j00zekTranslator(Converter, object):
    def __init__(self, LabelText):
        Converter.__init__(self, LabelText)
        self.translatedLabel  = translate(LabelText)

    @cached
    def getText(self):
        return self.translatedLabel
        
    text = property(getText)
