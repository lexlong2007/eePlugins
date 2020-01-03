#
# j00zek: this file has changed name to avoid errors using opkg (situation when file was installed by different package)
#          and uses skin own translations
#
from Components.Converter.Converter import Converter
from Components.Element import cached

class FluidNextTextToUpper(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = type

    @cached
    def getText(self):
        if self.type is not None:
            if self.source is not None:
                if self.source.text is not None:
                    return self.source.text.upper()
                else:
                    return ''
            else:
                return ''
        else:
            return ''
        return

    text = property(getText)