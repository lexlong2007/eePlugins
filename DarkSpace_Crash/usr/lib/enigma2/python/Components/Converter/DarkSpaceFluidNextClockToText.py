#
# j00zek: this file has changed name to avoid errors using opkg (situation when file was installed by different package)
#          and uses skin own translations
#
from time import localtime, strftime
from Components.Element import cached
from Converter import Converter

class DarkSpaceFluidNextClockToText(Converter, object):
    FORMAT = 0

    def __init__(self, type):
        Converter.__init__(self, type)
        self.fmt_string = type

    @cached
    def getText(self):
        time = self.source.time
        if time is None or time == -1 or time == -2:
            return ''
        else:
            t1 = localtime(time[0])
            t2 = localtime(time[1])
            return_str = '%s - %s' % (strftime(self.fmt_string, t1), strftime(self.fmt_string, t2))
            return return_str

    text = property(getText)