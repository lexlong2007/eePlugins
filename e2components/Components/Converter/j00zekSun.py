#
# j00zek 2018 
#
from enigma import eTimer
from Components.Converter.Converter import Converter
from Components.Element import cached

DBG = False
if DBG: from Components.j00zekComponents import j00zekDEBUG

class j00zekSun(Converter, object):
    def __init__(self, arg):
        Converter.__init__(self, arg)
        if DBG: j00zekDEBUG('[j00zekSun:__init__] >>>')
        self.checkTimer = eTimer()
        self.checkTimer.callback.append(self.checkKODIstate)
        self.checkTimer.start(1000) #check once a minute for tests

    @cached
    def getText(self):
        return ""

    text = property(getText)
    
    def checkKODIstate(self):
        if DBG: j00zekDEBUG('[j00zekSun:checkKODIstate] >>>')
        return
    
