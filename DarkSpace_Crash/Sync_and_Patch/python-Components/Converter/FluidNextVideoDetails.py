#
# j00zek: this file has changed name to avoid errors using opkg (situation when file was installed by different package)
#          and uses skin own translations
#
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, eTimer
from Components.Element import cached
import time, thread
from Poll import Poll
frqdic = {'23976': '24',
 '24000': '24',
 '25000': '25',
 '29970': '30',
 '30000': '30',
 '50000': '50',
 '59940': '60',
 '60000': '60'}

class FluidNextVideoDetails(Poll, Converter, object):
    changer = None
    VIDEO_DETAILS = 0

    def __init__(self, type):
        Poll.__init__(self)
        Converter.__init__(self, type)
        self.type = self.VIDEO_DETAILS
        self.changeTimer = eTimer()
        self.what = None
        self.interesting_events = (iPlayableService.evVideoSizeChanged,
         iPlayableService.evVideoProgressiveChanged,
         iPlayableService.evVideoFramerateChanged,
         iPlayableService.evUpdatedInfo,
         iPlayableService.evStart,
         iPlayableService.evTunedIn)
        return

    def getServiceInfoString(self, info, what, convert = lambda x: '%d' % x):
        v = info.getInfo(what)
        if v == -1:
            return 'N/A'
        if v == -2:
            return info.getInfoString(what)
        return convert(v)

    @cached
    def getText(self):
        service = self.source.service
        info = service and service.info()
        if not info:
            return ''
        yres = self.getServiceInfoString(info, iServiceInformation.sVideoHeight)
        xres = self.getServiceInfoString(info, iServiceInformation.sVideoWidth)
        fr = str(self.getServiceInfoString(info, iServiceInformation.sFrameRate))
        if str(fr) in frqdic:
            frame_rate = frqdic[str(fr)]
        else:
            frame_rate = ''
        progressive = self.getServiceInfoString(info, iServiceInformation.sProgressive)
        try:
            height = 0
            if int(xres) > 1920:
                height = 2160
            elif int(xres) > 1280:
                height = 1080
            elif int(xres) > 1270:
                height = 720
            elif int(yres) > 480:
                height = 576
            else:
                height = 480
            suffix = 'P'
            if str(progressive) == '0' and height != 720:
                suffix = 'i'
                if frame_rate != '':
                    frame_rate = 2 * int(frame_rate)
            val = '%s%s%s' % (str(height), suffix, str(frame_rate))
            return val
        except Exception as ex:
            return ''

    text = property(getText)

    @cached
    def getValue(self):
        service = self.source.service
        info = service and service.info()
        if not info:
            return -1
        if self.type == self.VIDEO_DETAILS:
            h = self.getServiceInfoString(info, iServiceInformation.sVideoHeight)
            r = self.getServiceInfoString(info, iServiceInformation.sFrameRate)
            p = self.getServiceInfoString(info, iServiceInformation.sProgressive)
            if h < 0 or r < 0 or p < 0:
                return -1
            else:
                return -2
        return -1

    value = property(getValue)

    def changed(self, what):
        if what[0] == self.CHANGED_SPECIFIC:
            if what[1] in self.interesting_events:
                Converter.changed(self, what)
        elif what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
            Converter.changed(self, what)
        elif what[0] == self.CHANGED_POLL:
            self.downstream_elements.changed(what)