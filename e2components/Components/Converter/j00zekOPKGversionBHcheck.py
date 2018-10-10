#
# j00zek 2018 
#
from enigma import eConsoleAppContainer, eTimer
from Components.Converter.Converter import Converter
from Components.Element import cached

DBG = True
if DBG: from Components.j00zekComponents import j00zekDEBUG

class j00zekOPKGversionBHcheck(Converter, object):
    def __init__(self, arg):
        Converter.__init__(self, arg)
        if DBG: j00zekDEBUG('[j00zekOPKGversionBHcheck:__init__] >>>')
        self.currVersion = '?'
        self.retstr = ''
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.appClosed)
        self.container.dataAvail.append(self.dataAvail)
        self.checkTimer = eTimer()
        self.checkTimer.callback.append(self.checkOPKG)
        self.checkTimer.start(30000, True) #check version with small delay after GUI starts

    @cached
    def getText(self):
        if DBG: j00zekDEBUG('[j00zekOPKGversionBHcheck:getText] self.currVersion=%s' % self.currVersion)
        return self.currVersion

    text = property(getText) 
    
    def checkOPKG(self):
        if DBG: j00zekDEBUG('[j00zekOPKGversionBHcheck:checkOPKG] >>>')
        self.checkTimer.stop() 
        self.retstr = ''
        cmd=[]
        cmd.append('opkg update > /dev/null')
        cmd.append('opkg list-installed|grep enigma2-plugin-skins--j00zeks-blackharmonyfhd')
        self.container.execute(";".join(cmd))
    
    def appClosed(self, retval):
        if DBG: j00zekDEBUG("[j00zekOPKGversionBHcheck:appClosed] retval=%s, retstr='%s'" % (str(retval), self.retstr))
        if self.retstr.find('enigma2-plugin-skins--j00zeks-blackharmonyfhd') >= 0:
            self.currVersion = self.retstr.replace('enigma2-plugin-skins--j00zeks-blackharmonyfhd','').split('-')[1].strip()
        self.retstr = ''
        if DBG: j00zekDEBUG("[j00zekOPKGversionBHcheck:appClosed] self.currVersion='%s'" % self.currVersion)

    def dataAvail(self, str):
        if DBG: j00zekDEBUG("[j00zekOPKGversionBHcheck:dataAvail] %s" % str)
        self.retstr += str 