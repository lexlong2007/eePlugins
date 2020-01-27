from Components.config import config
from Components.Element import cached
from Converter import Converter
from enigma import eTimer
from time import localtime, strftime
try:
    from boxbranding import getBoxType
except Exception:
    def getBoxType():
        return 'unknown'

class j00zekBlinkingClock(Converter, object):
    LEFT   = 0
    CENTER = 1
    RIGHT  = 2
    TVcfg  = 4
    VFDstdby = 5
    FMT = 6
    
    def __init__(self, type):
        Converter.__init__(self, type)
        self.BlinkTimer = eTimer()
        self.BlinkTimer.callback.append(self.blinkFunc)     
        self.BlinkTimer.start(1000)         
        self.CHAR = ":"
        if getBoxType() in ('ax51', 'vuduo', 'sf3038', 'sf4008', 'beyonwizu4', 'unknown'):
            self.VFDsize = 16
        else:
            self.VFDsize = 12
        if type == "clockVFDstdby":
            self.TYPE = self.VFDstdby
        else:
            self.TYPE = self.FMT
            self.fmt_string = type.replace('Format:','')

    def blinkFunc(self):
        if self.CHAR == ":" and self.TYPE == self.VFDstdby:
            self.CHAR = " "
        else:
            self.CHAR = ":"
        
    def doSuspend(self, suspended): 
        if suspended == 1: 
            self.BlinkTimer.stop()
        else: 
            self.BlinkTimer.start(1000)
            
    @cached
    def getText(self):
        time = self.source.time
        if time is None:
            return ""
        t = localtime(time)
        position = int(config.plugins.j00zekCC.clockVFDpos.value)
        if self.TYPE == self.VFDstdby:
            self.fmt_string = config.plugins.j00zekCC.clockVFDstdby.value

        ClockText = strftime(self.fmt_string, t)
        ClockTextLen = len(ClockText)
        
        if self.TYPE == self.VFDstdby and ClockTextLen <= self.VFDsize:
            ClockText = ClockText.replace(":", self.CHAR)
        if position == 2 or position == 3:
            Spaces = self.VFDsize - ClockTextLen
            if Spaces > 0:
                if position == 2: #center
                    ClockText = " " * int(Spaces/2) + ClockText
                elif position == 3: #right
                    ClockText = " " * Spaces + ClockText
        
        return ClockText

    text = property(getText)
