#
# j00zek 2018 
#
from enigma import eConsoleAppContainer, eTimer
from Components.Converter.Converter import Converter
from Components.Element import cached

DBG = False
if DBG: from Components.j00zekComponents import j00zekDEBUG

class j00zekOPKGupgradeCheck(Converter, object):
    def __init__(self, arg):
        Converter.__init__(self, arg)
        self.lastState = False
        self.currState = False
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.appClosed)
        self.container.dataAvail.append(self.dataAvail)
        self.checkTimer = eTimer()
        self.checkTimer.callback.append(self.checkOPKG)
        self.checkTimer.start(86400000) #check once a day = 1000ms * 60 * 60 * 24

    @cached
    def getBoolean(self):
        if DBG: j00zekDEBUG('[BlackHarmonyVersionConverter:getBoolean] self.lastState=%s' % self.lastState)
        return self.lastState

    boolean = property(getBoolean)
    
    def checkOPKG(self):
        if DBG: j00zekDEBUG('[BlackHarmonyVersionConverter:checkOPKG] >>>')
        cmd=[]
        cmd.append('opkg update')
        cmd.append('opkg list-upgradable')
        self.container.execute(";".join(cmd))
    
    def appClosed(self, retval):
        if DBG: j00zekDEBUG("[BlackHarmonyVersionConverter:appClosed] retval=%s" % str(retval))
        if self.lastState != self.currState:
            self.lastState = self.currState
            Converter.changed(self, (self.CHANGED_POLL,))

    def dataAvail(self, str):
        if DBG: j00zekDEBUG("[BlackHarmonyVersionConverter:dataAvail] %s" % str)
        if str.find('j00zek') > 0:
            self.currState = True
        else:
            self.currState = False
