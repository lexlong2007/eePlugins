# BlackHarmonyFanTempInfo Converter  v.0.4

from Poll import Poll
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists

class BlackHarmonyFanTempInfo(Poll, Converter, object):
    FanInfo = 0
    TempInfo = 1
    TempInfoHeader = 3
    FanInfoHeader = 4
    
    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        if type == "FanInfo":
            self.type = self.FanInfo
        elif type == "TempInfo":
            self.type = self.TempInfo
        self.poll_interval = 2000
        self.poll_enabled = True
        if fileExists("/proc/stb/fp/fan_speed"):
            self.FanHeader = 'FAN:'
        else:
            self.FanHeader = ''
            
        self.TempHeader = ''
        self.TempUnit = ''
        if fileExists("/proc/stb/sensors/temp0/value") and fileExists("/proc/stb/sensors/temp0/unit"):
            self.TempPath = "/proc/stb/sensors/temp0/value"
            self.TempHeader = 'TMP:'
            self.TempUnit = open("/proc/stb/sensors/temp0/unit").read().strip('\n')
        elif fileExists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
            try:
                open("/sys/devices/virtual/thermal/thermal_zone0/temp").read() #check if it can be read, onsolo4k it doesn't
                self.TempPath = "/proc/stb/sensors/temp0/value"
                self.TempHeader = 'TMP:'
                self.TempUnit = 'C'
            except Exception:
                pass
    
    @cached
    def getText(self):
        try:
            if self.type == self.FanInfoHeader:
                    return self.FanHeader
            elif self.type == self.FanInfo and self.FanHeader != '':
                return open("/proc/stb/fp/fan_speed").read().strip('\n')
            elif self.type == self.TempInfoHeader:
                    return self.TempHeader
            elif self.type == self.TempInfo and self.TempHeader != '':
                return "%s%s%s" % (open().read(self.TempPath).strip('\n')[:2], unichr(176).encode("latin-1"), self.TempUnit )
        except Exception:
            pass
        return ''
    
    text = property(getText)
    
    def changed(self, what):
        if what[0] == self.CHANGED_POLL:
            self.downstream_elements.changed(what)
