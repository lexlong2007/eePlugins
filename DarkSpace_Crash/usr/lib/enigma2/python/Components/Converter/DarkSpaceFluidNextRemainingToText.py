#
# j00zek: this file has changed name to avoid errors using opkg (situation when file was installed by different package)
#          and uses skin own translations
#
from Components.Converter.Converter import Converter
from Components.Element import cached

class DarkSpaceFluidNextRemainingToText(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)

    @cached
    def getText(self):
        time = self.source.time
        if time is None:
            return ''
        else:
            duration, remaining = self.source.time
            if remaining is not None:
                return '+%d min/%d min' % (remaining / 60, duration / 60)
            return '%d min' % (duration / 60)
            return

    text = property(getText)